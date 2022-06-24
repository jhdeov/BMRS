#from Formulas.HToneSpreadPenult import *

from importlib import import_module

class Input:
    def __init__(self,word,bmrs):
        #Given a word and bmrs file, we start to set up the system
        self.importedModule = import_module(bmrs)


        # if the input word was a string like "LLL", then we turn it into a list with word boundaries
        # ["#, "L", "L", "L", "%"]
        # We do this so that we have a single representation for string inputs and feature inputs
        if type(word) is str: word = list(word)
        self.word=['#'] + word + ['%']

        ####
        # Before we read the BMRS file, we set up the attributes that will be filled by the BMRS file
        self.copyset=None
        self.input_symbols = []
        self.labels_list=[]
        self.labels_are_input = True

        self.importedModule.personal_setup(self)
        if self.labels_are_input: self.associate_symbols_to_labels()
        else: self.importedModule.personal_features(self)
        self.functions_list = ['succ', 'pred']

        #Verify that the input string uses only legal characters
        for symbol in word:
            if type(symbol) is str and symbol not in self.input_symbols:
                    print(f'Error, your input string has an illegal character ' + str(symbol))
                    exit()
            #More bookkeeping if the input symbol is a feature bundle
            elif type(symbol) is list:
                for feature in symbol:
                    if feature not in self.input_symbols:
                        print(f'Error, your input string has an illegal character ' + str(symbol))
                        exit()
        #Given the above set of IPA symbols and features, we map the input word into a matrix of feature values and
        #successor/predecessor values
        self.create_domain()
        self.create_input_labels()
        self.create_input_functions()



        self.create_input_display()



        #Intiailize the output structure to a matrix of Nothing, same for input predicates
        self.predicates_list=[]
        self.importedModule.personal_predicate_setup(self)
        self.create_input_predicates()

        self.create_output_labels()
        self.create_output_functions()

        #easier to just let user specify the changes
        # self.faithful_labels=self.initialize_empty_dict(self.copyset)
        # self.changed_labels=self.initialize_empty_dict(self.copyset)
        # self.false_labels = self.initialize_empty_dict(self.copyset)
        #
        self.faithful_functions = self.initialize_empty_dict(self.copyset)
        # self.changed_functions = self.initialize_empty_dict(self.copyset)
        # self.false_functions=self.initialize_empty_dict(self.copyset)

        for copy in self.copyset:
            self.faithful_functions[copy]=self.functions_list

        """ ----------"""
        self.preprocess_output()

        self.fill_output()

        #Add output to display
        self.create_output_display()

        #turn features back into segments and add to display
        self.create_output_segments()
        self.create_output_segments_display()

        self.print_display()

    ##Old way of keeping track of changed/removed/true features
    # def personal_changes(self):
    #
    #     ##Copy 1:
    #     # self.changed_labels[1] = ['voiced']
    #     # self.faithful_labels[1] =  [label for label in self.labels_list if label not in self.changed_labels[1]]
    #     # self.false_labels[1] = []
    #
    #     # self.changed_functions[1] = []
    #     self.faithful_functions[1] = self.functions_list
    #     # self.changed_functions[1] = []

    def associate_symbols_to_labels(self):
        #This is redundant if your inputs are the same as your labels
        #But we need to do this so that both phonological strings and non-featured strings will work with the same
        #create_input_labels method
        self.symbol_to_labels = {}
        for label in self.labels_list:
            self.symbol_to_labels[label] = frozenset([label])
        self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}

    def create_domain(self):
        self.domain_size = len(self.word)
        self.domain_elements = list(range(self.domain_size))

    def create_input_labels(self):
        self.input_to_labels = {}
        for label in self.labels_list:
            self.input_to_labels[label] = self.initialize_empty_dict(self.domain_elements)
        for index in self.domain_elements:
            segment = self.word[index]
            for label in self.labels_list:
                self.input_to_labels[label][index] = False
            #Need to do some tricks if the domain element has a list of features, e.g., a feature bundle of case and number
            #Check if the segment is a feature bundle; if yes, then give it each of those features via for-loop
            segment_features=frozenset([])
            if type(segment) is list:
                for feature in segment:
                    segment_features = segment_features.union(self.symbol_to_labels[feature])
            else:
                segment_features = self.symbol_to_labels[segment]
            for feature in segment_features:
                self.input_to_labels[feature][index] = True

    def create_input_predicates(self):
        self.input_to_predicates={}
        for predicate in self.predicates_list:
            self.input_to_predicates[predicate] = self.initialize_empty_dict(self.domain_elements)
        # for index in self.domain_elements:
        #     segment = self.word[index]
        #     for predicate in self.predicates_list:
        #         self.input_to_predicates[predicate][index] = False
        #     segment_features = self.symbol_to_labels[segment]
        #     for feature in segment_features:
        #         self.input_to_labels[feature][index] = True


    def create_input_functions(self):
        self.input_to_functions = {}
        self.input_to_functions['succ'] = self.initialize_empty_dict(self.domain_elements)
        self.input_to_functions['pred'] = self.initialize_empty_dict(self.domain_elements)
        for index in range(len(self.word) - 1):
            self.input_to_functions['succ'][index] = index + 1
        for index in range(1, len(self.word)):
            self.input_to_functions['pred'][index] = index - 1
        self.input_to_functions['pred'][0] = None
        self.input_to_functions['succ'][self.domain_size - 1] = None

    def initialize_empty_dict(self,some_list):
        empty_dict = {}
        for element in some_list:
            empty_dict[element] = None
        return empty_dict

    def initialize_copies(self,some_list):
        empty_copies= {}
        for copy in self.copyset:
            empty_copies[copy]=self.initialize_empty_dict(some_list)
        return empty_copies


    def create_input_display(self):
        self.display = []
        first_line = [''] + self.word
        second_line = [''] + self.domain_elements
        self.display = [first_line, second_line]
        self.display.append(['-'] * (self.domain_size + 1))
        for label in self.input_to_labels.keys():
            line = [label] + list(self.input_to_labels[label].values())
            self.display.append(line)
        for function in self.input_to_functions.keys():
            line = [function] + list(self.input_to_functions[function].values())
            self.display.append(line)
        self.display.append(['-'] * (self.domain_size + 1))


    def create_output_labels(self):
        self.output_to_labels = self.initialize_copies(self.labels_list)
        for copy in self.output_to_labels.keys():
            for label in self.labels_list:
                self.output_to_labels[copy][label] = self.initialize_empty_dict(self.domain_elements)

    def create_output_functions(self):
        self.output_to_functions =  self.initialize_copies(self.functions_list)
        for copy in self.output_to_labels.keys():
            for function in self.functions_list:
                self.output_to_functions[copy][function] = self.initialize_empty_dict(self.domain_elements)



    def preprocess_output(self):
        for copy in self.copyset:
            #Less book-keeping if I just make the labels handled by the user
            # for label in self.faithful_labels[copy]:
            #     for domain_element in self.domain_elements:
            #         self.output_to_labels[copy][label][domain_element]= self.input_to_labels[label][domain_element]
            # for label in self.false_labels[copy]:
            #     for domain_element in self.domain_elements:
            #         self.output_to_labels[copy][label][domain_element]= False
            for function in self.faithful_functions[copy]:
                for domain_element in range(self.domain_size):
                    self.output_to_functions[copy][function][domain_element] =  self.input_to_functions[function][domain_element]

    def fill_output(self):

        print('This is a log of all evaluations.')
        for copy in self.copyset:
            print("\tEvaluating elements in Copy ",copy)
            ##Will do all labels isntead ofjust changed labels
            #for label in self.changed_labels[copy]:
            for label in self.labels_list:
                print('\t\tEvaluating elements with the label ' + str(label))
                for domain_element in self.domain_elements:
                    print('\t\t\tEvaluating for the element ' + str(domain_element))
                    if self.output_to_labels[copy][label][domain_element] is None:
                        #self.get_output_value(copy, label, domain_element)
                        self.get_value(copy, 'label',label, domain_element)
                    print()

    # def get_output_value(self,copy,label,domain_element):
    #     """ get value returns the value of an output node just in case the output formula references another output formula """
    #     """always use get when spanning over domain elelemts"""
    #     print("entered get output; let's check if the domain element is None or outside the word")
    #     if domain_element is None: return False
    #     elif domain_element<0 or domain_element>=len(self.word): return False
    #
    #     print("Not none.")
    #     print(f'Doing get output value for copy {copy}, label {label}, domain element {domain_element} for input symbol'
    #           f'{self.word[domain_element]}')
    #
    #     if self.output_to_labels[copy][label].get(domain_element) is not None:
    #         print("I entered the not-null escape")
    #         return self.output_to_labels[copy][label][domain_element]
    #
    #     # print('gonna find pred and succ: ')
    #     pred = self.input_to_functions['pred'].get(domain_element)
    #     succ = self.input_to_functions['succ'].get(domain_element)
    #
    #
    #     found=personal_Output_Formula(self,copy,label,domain_element)
    #     print('returned output value was ' + str(found))
    #     self.output_to_labels[copy][label][domain_element] = found
    #     return found
    #
    # def get_predicate_value(self,predicate,domain_element):
    #     """ get value returns the value of a predicate over the input domain element"""
    #     """always use get when spanning over domain elelemts"""
    #     print("entered get pred; let's check if the domain element is None or outside the word")
    #     if domain_element is None: return False
    #     elif domain_element<0 or domain_element>=len(self.word): return False
    #
    #     print("Not none.")
    #     print(f'Doing get predicate for predicate {predicate}, domain element {domain_element} for input symbol'
    #           f'{self.word[domain_element]}')
    #     if self.input_to_predicates[predicate].get(domain_element) is not None:
    #         print("I entered the not-null escape")
    #         return self.input_to_predicates[predicate][domain_element]
    #
    #     print('going before the found for predicate: '+str(predicate))
    #     found=personal_Predicate_Formula(self,predicate,domain_element)
    #     print('returned predicate value was ' + str(found))
    #     self.input_to_predicates[predicate][domain_element] = found
    #     print('i set up the predicate:')
    #     print(self.input_to_predicates)
    #     return found

    def get_value(self,level,type,name,domain_element):
        if not ( level in ['input'] or level in self.copyset):
            print("Error, wrong level given to get_value. Must be `input' or a copy")
            print(f'{level}')
            exit()
        if not (type in ['label','function','predicate']):
            print("Error, wrong type given to get_value. Must be 'label', 'function', or 'predicate'")
            print(f'{type}')

            exit()
        if (type == 'label' and name not in self.input_to_labels) or \
            (type == 'function' and name not in self.input_to_functions) or \
            (type == 'predicate' and name not in self.input_to_predicates):
            print(f'Error, the {type} {name} is not an existing {type}')
            exit()


        if domain_element is None: return False
        if domain_element not in self.domain_elements:
            print("\t\t\t\tThe domain element is None or does not exist in the domain")
            print("\t\t\t\tReturning value of False")
            return False


        print(f'\t\t\t\tEvaluating get for level {level}, type {type}, name {name}, domain element {domain_element} for input symbol '
              f'{self.word[domain_element]}')


        if level == 'input':
            if type == 'label': return self.input_to_labels[name].get(domain_element)
            elif type =="function": return self.input_to_functions[name].get(domain_element)
            elif type == 'predicate':
                if self.input_to_predicates[name].get(domain_element) is not None:
                    print("\t\t\t\t\tThe value was already evaluated in a previous get")
                    return self.input_to_predicates[name][domain_element]
                print('\t\t\t\t\tWill evaluate the predicate using the user predicate list for: '  + str(name))

                found = self.importedModule.personal_Predicate_Formula(self, name, domain_element)
                print('\t\t\t\t\tReturned predicate value for '+str(name)+' was: ' + str(found))
                if found is None:
                    print('\t\t\t\t\tThe value is None so its set to false')
                    self.input_to_predicates[name][domain_element] = False
                else:
                    self.input_to_predicates[name][domain_element] = found
                return found

        if level in self.copyset:
            if type == 'label':
                if self.output_to_labels[level][name].get(domain_element) is not None:
                    print("\t\t\t\t\tThe value was already evaluated in a previous get")
                    return self.output_to_labels[level][name][domain_element]
                else:
                    print('\t\t\t\t\tWill evaluate the output label using the user label list for: ' + str(name))
                    found = self.importedModule.personal_Output_Formula(self, level, name, domain_element)
                    print('\t\t\t\t\tReturned output label value was: ' + str(found))
                    if found is None:
                        print('\t\t\t\t\tThe value is None so its set to false')
                        self.output_to_labels[level][name][domain_element] = False
                    else:
                        self.output_to_labels[level][name][domain_element] = found
                    return found

            elif type =="function":
                if self.output_to_functions[level][name].get(domain_element) is not None:
                    print("\t\t\t\t\tThe value was already evaluated in a previous get")
                    return self.output_to_functions[level][name][domain_element]
                else:
                    found = self.importedModule.personal_Output_Formula(self, level, name, domain_element)
                    print('\t\t\t\t\tReturned output function value was: ' + str(found))
                    if found is None:
                        print('\t\t\t\t\tThe value is None so its set to false')
                        self.output_to_functions[level][name][domain_element]  = False
                    else:
                        self.output_to_functions[level][name][domain_element]  = found
                    return found



    def create_output_display(self):
        self.display.append(['<pred>'] * (self.domain_size + 1))
        for predicate in self.input_to_predicates.keys():
            line = [predicate] + list(self.input_to_predicates[predicate].values())
            self.display.append(line)
        self.display.append(['-'] * (self.domain_size + 1))

        for copy in self.copyset:
            self.display.append(['<'+str(copy)+'>'] * (self.domain_size + 1))
            for label in self.output_to_labels[copy].keys():
                line = [label] + list(self.output_to_labels[copy][label].values())
                self.display.append(line)
            for function in self.output_to_functions[copy].keys():
                line = [function] + list(self.output_to_functions[copy][function].values())
                self.display.append(line)
            self.display.append(['-'] * (self.domain_size + 1))

    def create_output_segments(self):
        self.output_segments= self.initialize_empty_dict(self.copyset)
        for copy in self.output_segments.keys():
            self.output_segments[copy]=self.initialize_empty_dict(self.domain_elements)
        for copy in self.output_segments.keys():
            for element in self.domain_elements:
                features=[]
                for label in self.output_to_labels[copy]:
                    if self.output_to_labels[copy][label][element]==True: features.append(label)
                features=frozenset(features)
                if len(features)>0:
                    print("Will output the symbol at copy-element "+str(copy)+" "+str(element))
                    self.output_segments[copy][element]=self.labels_to_symbols[features]
                else: self.output_segments[copy][element]=''

    def create_output_segments_display(self):
        for copy in self.output_segments.keys():
            self.display.append([''] + list(self.output_segments[copy].values()))

    def print_display(self):
        for row in self.display:
            print(*row, sep='\t')




