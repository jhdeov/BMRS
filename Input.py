from Formulas.Bhaskar_even_a import *

class Input:
    def __init__(self,word):
        self.word='#' + word + '%'
        self.copyset=None
        self.labels_list=[]
        self.labels_are_input = True

        personal_setup(self)
        if self.labels_are_input: self.associate_symbols_to_labels()
        else: personal_features(self)
        self.functions_list = ['succ', 'pred']



        #Given the above set of IPA symbols and features, we map the input word into a matrix of feature values and
        #successor/predecessor values
        self.create_domain()
        self.create_input_labels()
        self.create_input_functions()



        self.create_input_display()

        self.print_display()

        #Intiailize the output structure to a matrix of Nothing, same for input predicates
        self.predicates_list=[]
        personal_predicate_setup(self)
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
        first_line = [''] + list(self.word)
        second_line = [''] + list(range(self.domain_size))
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

        print('will start filling table')
        print('I assume the output doesnt contain word boundaries')
        for copy in self.copyset:
            print("will start filling for copy",copy)
            ##Will do all labels isntead ofjust changed labels
            #for label in self.changed_labels[copy]:
            for label in self.labels_list:
                print('start filling for label ' + str(label))
                for domain_element in self.domain_elements:
                    print('start filling for element ' + str(domain_element))
                    if label in ['#','%']:
                        self.output_to_labels[copy][label][domain_element] = False
                    if self.output_to_labels[copy][label][domain_element] is None:
                        self.get_output_value(copy, label, domain_element)



    def get_output_value(self,copy,label,domain_element):
        """ get value returns the value of an output node just in case the output formula references another output formula """
        """always use get when spanning over domain elelemts"""
        print("entered get output; let's check if the domain element is None or outside the word")
        if domain_element is None: return False
        elif domain_element<0 or domain_element>=len(self.word): return False

        print("Not none. Doing get for copy-label-domain at input symbol "),print(copy,label,domain_element,self.word[domain_element])
        if self.output_to_labels[copy][label].get(domain_element) is not None:
            print("I entered the not-null escape")
            return self.output_to_labels[copy][label][domain_element]

        # print('gonna find pred and succ: ')
        pred = self.input_to_functions['pred'].get(domain_element)
        succ = self.input_to_functions['succ'].get(domain_element)


        found=personal_Output_Formula(self,copy,label,domain_element)
        print('returned output value was ' + str(found))
        self.output_to_labels[copy][label][domain_element] = found
        return found

    def get_predicate_value(self,predicate,domain_element):
        """ get value returns the value of a predicate over the input domain element"""
        """always use get when spanning over domain elelemts"""
        print("entered get pred; let's check if the domain element is None or outside the word")
        if domain_element is None: return False
        elif domain_element<0 or domain_element>=len(self.word): return False

        print("Not none. Doing get for predicate-domain at input symbol ")
        print(predicate,domain_element,self.word[domain_element])
        if self.input_to_predicates[predicate].get(domain_element) is not None:
            print("I entered the not-null escape")
            return self.input_to_predicates[predicate][domain_element]

        print('going before the found for predicate:'+str(predicate))
        found=personal_Predicate_Formula(self,predicate,domain_element)
        print('returned predicate value was ' + str(found))
        self.input_to_predicates[predicate][domain_element] = found
        print('i set up the predicate:')
        print(self.input_to_predicates)
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
                    self.output_segments[copy][element]=self.labels_to_symbols[features]
                else: self.output_segments[copy][element]=''

    def create_output_segments_display(self):
        for copy in self.output_segments.keys():
            self.display.append([''] + list(self.output_segments[copy].values()))

    def print_display(self):
        for row in self.display:
            print(*row, sep='\t')




