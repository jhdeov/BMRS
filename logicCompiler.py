#from Formulas.HToneSpreadPenult import *
import sys
from importlib import import_module

class logicCompilation:
    def __init__(self,word,bmrs):


        self.bmrs= bmrs
        self.importedModule = import_module(bmrs)

        print("Useful debugging info for conversion is printed into the running.message.log")
        # The printing code was taken from https://stackoverflow.com/a/2513511
        old_stdout = sys.stdout
        log_file = open(bmrs + ".running.message.log", "w")
        sys.stdout = log_file

        #Given a word and bmrs file, we start to set up the system
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
        self.inputIsString = True # TODO incorporate variation
        self.isOrderPreserving = True # TODO incorporate variation


        self.importedModule.personal_setup(self)
        if self.labels_are_input: self.associate_symbols_to_labels()
        else: self.importedModule.personal_features(self)
        if self.inputIsString:
            self.functions_list = ['succ', 'pred']
        else:
            print(f'TODO')
            exit()
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
        #Given the above set of IPA symbols and features, we map the input graph and output graph into a matrix of feature values and
        #successor/predecessor values.
        self.create_domain()
        self.graphNodeList = self.create_nodesAsList([0] + self.copyset)
        self.create_labels()
        self.create_functions()

        # Intiailize the output structure to a matrix of Nothing, same for input predicates
        self.predicates_list = []
        self.importedModule.personal_predicate_setup(self)
        self.create_input_predicates()
        
        # Start creating the display graph for the input
        self.create_input_display()

        # Fill up the output graph with succ/pred functions if output-preserving
        self.initializeOutputFunctions()

        self.fill_output()

        #Add output to display
        self.create_output_display()

        #turn features back into segments and add to display
        self.create_output_segments()
        self.create_output_segments_String()

        sys.stdout = old_stdout
        log_file.close()
        self.print_display()



    def associate_symbols_to_labels(self):
        #This is redundant if your inputs are the same as your labels
        #But we need to do this so that both phonological strings and non-featured strings will work with the same
        #create_labels method
        self.symbol_to_labels = {}
        for label in self.labels_list:
            self.symbol_to_labels[label] = frozenset([label])
        self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}

    def create_domain(self):
        self.domain_size = len(self.word)
        self.domain_elements = list(range(self.domain_size))
    def create_nodesAsList(self, levels):
        nodeList = []
        for level in levels:
            for domain_element in range(self.domain_size):
                nodeList.append((level, domain_element))
        return nodeList
    def create_nodesAsDict(self, levels):
        nodeDict = {}
        for level in levels:
            for domain_element in range(self.domain_size):
                nodeDict[(level, domain_element)] = None
        return nodeDict
    def create_labels(self):
        self.labels_for_nodes = {}
        for label in self.labels_list:
            self.labels_for_nodes[label] = self.initialize_empty_dict(self.graphNodeList)
        for index in self.domain_elements:
            segment = self.word[index]
            for label in self.labels_list:
                self.labels_for_nodes[label][(0,index)] = False
            #Need to do some tricks if the domain element has a list of features, e.g., a feature bundle of case and number
            #Check if the segment is a feature bundle; if yes, then give it each of those features via for-loop
            segment_features=frozenset([])
            if type(segment) is list:
                for feature in segment:
                    segment_features = segment_features.union(self.symbol_to_labels[feature])
            else:
                segment_features = self.symbol_to_labels[segment]
            for feature in segment_features:
                self.labels_for_nodes[feature][(0,index)] = True

    def create_input_predicates(self):
        self.predicates_for_nodes={}
        for predicate in self.predicates_list:
            self.predicates_for_nodes[predicate] = self.initialize_empty_dict(self.graphNodeList)

    def create_functions(self):
        if self.inputIsString:
            self.functions_for_nodes = {}
            self.functions_for_nodes['succ'] = self.initialize_empty_dict(self.graphNodeList)
            self.functions_for_nodes['pred'] = self.initialize_empty_dict(self.graphNodeList)
            for index in range(len(self.word) - 1):
                self.functions_for_nodes['succ'][(0,index)] = (0,index + 1)
            for index in range(1, len(self.word)):
                self.functions_for_nodes['pred'][(0,index)] = (0,index - 1)
            # As a trick, we distinguish between None which means the function was not checked
            # vs. (None,None) which means the function was evaluated to return nothing
            self.functions_for_nodes['pred'][(0,0)] = (None,None)
            self.functions_for_nodes['succ'][(0,self.domain_size - 1)] = (None,None)
        else:
            print(f'TODO')
            exit()
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

        for label in self.labels_for_nodes.keys():
            line = [label]
            for domain_element in self.domain_elements:
                line = line +  [self.labels_for_nodes[label][(0,domain_element)]]
            self.display.append(line)
        for function in self.functions_for_nodes.keys():
            line = [function]
            for domain_element in self.domain_elements:
                line = line + [self.functions_for_nodes[function][(0, domain_element)]]
            self.display.append(line)
        self.display.append(['-'] * (self.domain_size + 1))



    def initializeOutputFunctions(self):
        #This will populate the succ/pred values of the outgraph with either None if non-order-preserving
        # otherwise with order-preserving values
        #TODO: incorporate non-string functions
        print("Pre-processing order-preservation succ/pred relations for all nodes")
        for copyindex in range(len(self.copyset)):
            current_copy = self.copyset[copyindex]
            for function in self.functions_for_nodes.keys():
                for domain_element in range(self.domain_size):
                    if not self.isOrderPreserving:
                        self.functions_for_nodes[function][(current_copy,domain_element)] =  None
                    else:
                        assert function == 'succ' or function == 'pred'
                        if len(self.copyset) is 1:
                            if self.functions_for_nodes[function][(0,domain_element)] ==  (None,None):
                                self.functions_for_nodes[function][(current_copy,domain_element)] =  (None,None)
                            else:
                                self.functions_for_nodes[function][(current_copy,domain_element)] = \
                                    (current_copy,self.functions_for_nodes[function][(0,domain_element)][1])
                        elif copyindex is len(self.copyset)-1: # copyindex is final
                            previous_copy = self.copyset[copyindex-1]
                            first_copy= self.copyset[0]
                            if function == 'succ':
                                if self.functions_for_nodes[function][(0,domain_element)] ==   (None,None):
                                    self.functions_for_nodes[function][(current_copy,domain_element)] =  (None,None)
                                else:
                                    self.functions_for_nodes[function][(current_copy,domain_element)] = \
                                       (first_copy, self.functions_for_nodes[function][(0,domain_element)][1])
                            elif function == 'pred':
                                self.functions_for_nodes[function][(current_copy,domain_element)] = \
                                     (previous_copy, domain_element)
                        elif copyindex is 0:##copyindex is initial
                            current_copy = self.copyset[copyindex]
                            next_copy = self.copyset[copyindex + 1]
                            last_copy = self.copyset[-1]
                            if function == 'succ':
                                self.functions_for_nodes[function][(current_copy,domain_element)] = \
                                        (next_copy, domain_element)
                            elif function == 'pred':
                                if self.functions_for_nodes[function][(0,domain_element)] == (None,None):
                                    self.functions_for_nodes[function][(current_copy,domain_element)] =  (None,None)
                                else:
                                    self.functions_for_nodes[function][(current_copy,domain_element)] = \
                                        (last_copy, self.functions_for_nodes[function][(0,domain_element)][1])
                        else:
                            current_copy = self.copyset[copyindex]
                            next_copy = self.copyset[copyindex + 1]
                            if function == 'succ':
                                self.functions_for_nodes[function][(current_copy,domain_element)] = \
                                    (next_copy, domain_element)
                            elif function == 'pred':
                                self.functions_for_nodes[function][(current_copy,domain_element)] = \
                                    (first_copy, self.functions_for_nodes[function][(0,domain_element)][1])

        print(f"Established the following functions for the output:\n{self.functions_for_nodes}")
    def fill_output(self):

        print('This is a log of all evaluations.')
        for copy in self.copyset:
            print("\tEvaluating elements in Copy ",copy)
            ##Will do all labels isntead ofjust changed labels
            #for label in self.changed_labels[copy]:
            for label in self.labels_list:
                print(f'\t\tEvaluating elements with the label {label} in copy {copy}')
                for domain_element in self.domain_elements:
                    print(f'\t\t\tEvaluating for the element {domain_element} in copy {copy}')
                    if self.labels_for_nodes[label][(copy,domain_element)] is None:
                        #OLD self.get_value(copy, 'label',label, domain_element)
                        self.get_BooleanValue('label',label, (copy, domain_element))
                    print()
        print("We will find all output nodes that have labels")
        self.findOvertOutput()

        if self.inputIsString and not self.isOrderPreserving:
            print(f"The transduction is not order-preserving, so we  must determine all the succ/pred relations"
                  f"\nWe determine succ/pred of output nodes that have labels")
            for copy in self.copyset:
                print("\tEvaluating elements in Copy ", copy)
                for function in self.functions_list:
                    print(f'\t\tEvaluating elements with the function {function} in copy {copy}')
                    for domain_element in self.domain_elements:
                        print(f'\t\t\tEvaluating for the element {domain_element} in copy {copy}')
                        if (copy,domain_element) in self.overtOutputSegments.keys():
                            print("\t\t\t\tThis output element is an overt segment so we can find its succ/pred functions")
                            if self.functions_for_nodes[function][(copy, domain_element)] is None:
                                # OLD self.get_value(copy, 'function', function, domain_element)
                                self.get_NodeValue( 'function', function,(copy, domain_element))
                        else:
                            print("\t\t\t\tThis output element is not an overt segment so we skip its succ/pred functions")

        self.cleanUpStringPath()
    def findOvertOutput(self):
        self.overtOutputSegments = {}
        for copy in self.copyset:
            for element in self.domain_elements:
                features=[]
                for label in self.labels_for_nodes.keys():
                    if self.labels_for_nodes[label][(copy,element)]==True: features.append(label)
                features=frozenset(features)
                if len(features)>0:
                    print("\tFound an overt output segment at copy-element "+str(copy)+" "+str(element))
                    self.overtOutputSegments[(copy,element)]=self.labels_to_symbols[features]
        print(f'Found the following list of overt output segments:\n\t{self.overtOutputSegments}')


# OLD    def get_value(self,level,typeLogic,name,domain_element):
#         if not ( level in ['input'] or level in self.copyset):
#             print("Error, wrong level given to get_value. Must be `input' or a copy")
#             print(f'{level}')
#             exit()
#         if not (typeLogic in ['label','function','predicate']):
#             print("Error, wrong type given to get_value. Must be 'label', 'function', or 'predicate'")
#             print(f'{typeLogic}')
#
#             exit()
#         if (typeLogic == 'label' and name not in self.labels_for_nodes.keys()) or \
#             (typeLogic == 'function' and name not in self.functions_for_nodes.keys()) or \
#             (typeLogic == 'predicate' and name not in self.predicates_for_nodes.keys()):
#             print(f'Error, the {typeLogic} {name} is not an existing {typeLogic}')
#             exit()
#
#         # if type(domain_element) is tuple:
#         #     print(f'Error, the domain_element is a tuple {domain_element}, but it should just be the second integer')
#         #     exit()
#
#         if domain_element is None:
#             print(f"\t\t\t\tThe domain element {domain_element} is None, which means we return False")
#             return False
#
#         if not (domain_element == (None,None) or domain_element in self.domain_elements):
#             print(f"\t\t\t\The domain element {domain_element} does not exist in the domain\n"
#                   f"Nor is it the empty output node (None,None)\n"
#                   f"Returning False")
#             return False
#             # TODO not sure if such a situation can ever arise and be correct
#
#         print(f'\t\t\t\tEvaluating get for level {level}, type {typeLogic}, name {name}, domain element {domain_element}')
#         ##for input symbol   {self.word[domain_element]}')
#
#
#         if level == 'input':
#             if typeLogic == 'label':
#                 returnValue = self.labels_for_nodes[name].get((0,domain_element))
#                 print(f'\t\t\t\t\tReturning an input label value {returnValue}')
#                 return returnValue
#             elif typeLogic =="function":
#                 returnValue = self.functions_for_nodes[name].get((0,domain_element))
#                 print(f'\t\t\t\t\tReturning an input function value {returnValue}')
#                 return returnValue
#             elif typeLogic == 'predicate':
#                 if self.predicates_for_nodes[name].get((0,domain_element)) is not None:
#                     returnValue = self.predicates_for_nodes[name][(0,domain_element)]
#                     print("\t\t\t\t\tThe value was already evaluated in a previous get")
#                     print(f'\t\t\t\t\tReturning an input predicate value {returnValue}')
#                     return returnValue
#                 print('\t\t\t\t\tWill evaluate the predicate using the user predicate list for: '  + str(name))
#                 found = self.importedModule.personal_Predicate_Formula(self, name, domain_element)
#                 print(f'hi {found}')
#                 print('\t\t\t\t\tReturned predicate value for '+str(name)+' was: ' + str(found))
#                 if found is None:
#                     print('\t\t\t\t\tThe value is None so its set to false')
#                     self.predicates_for_nodes[name][(0,domain_element)] = False
#                 else:
#                     self.predicates_for_nodes[name][(0,domain_element)] = found
#                 return found
#
#         if level in self.copyset:
#             if typeLogic == 'label':
#                 if self.labels_for_nodes[name].get((level,domain_element)) is not None:
#                     print("\t\t\t\t\tThe value was already evaluated in a previous get")
#                     return self.labels_for_nodes[name][(level,domain_element)]
#                 else:
#                     print('\t\t\t\t\tWill evaluate the output label using the user label list for: ' + str(name))
#                     found = self.importedModule.personal_OutputLabel_Formula(self, level, name, domain_element)
#                     print('\t\t\t\t\tReturned output label value was: ' + str(found))
#                     if found is None:
#                         print('\t\t\t\t\tThe value is None so its set to false')
#                         self.labels_for_nodes[name][(level,domain_element)] = False
#                     else:
#                         self.labels_for_nodes[name][(level,domain_element)] = found
#                     return found
#
#             elif typeLogic =="function":
#                 if self.functions_for_nodes[name].get((level,domain_element)) is not None:
#                     print("\t\t\t\t\tThe value was already evaluated in a previous get")
#                     return self.functions_for_nodes[name][(level,domain_element)]
#                 else:
#                     found = self.importedModule.personal_OutputFunction_Formula(self, level, name, domain_element)
#                     print('\t\t\t\t\tReturned output function value was: ' + str(found))
#                     if found is None:
#                         print('\t\t\t\t\tThe value is None so its set to (None,None)')
#                         found = (None,None)
#                     elif type(found) is tuple and found[1] ==  None:
#                         print('\t\t\t\t\tThe value is (level,None) so its set to (None,None)')
#                         found = (None,None)
#                     assert type(found) is tuple
#                     self.functions_for_nodes[name][(level,domain_element)]  = found
#                     return found

    def get_BooleanValue(self,typeLogic,name,node):
        level,domain_element = node
        if (level, domain_element) == None:
            print(
                f"\t\t\tThe level and domain element {level, domain_element} is None, which means we return False by default"
                f"TODO test break")
            exit()
            return False
        if level == None and domain_element == None:
            print(f"\t\t\tThe node is  {node}, which is the empty non-existent node\n"
                  f"\t\t\tBy default, we return false")
            return False
        if not (domain_element == (None, None) or domain_element in self.domain_elements):
            print(f"\t\t\tThe domain element {domain_element} does not exist in the domain\n"
                  f"Nor is it the empty output node (None,None)\n"
                  f"TODO not sure if such a situation can ever arise and be correct")
            exit()
            return False

        if not ( level in [0] or level in self.copyset):
            print("\t\t\tError, wrong level given to get_BooleanValue. Must be 0 or a copy")
            print(f'{level}')
            exit()
        if not (typeLogic in ['label','predicate']):
            print("\t\t\tError, wrong type given to get_BooleanValue. Must be 'label' or 'predicate'")
            print(f'{typeLogic}')

            exit()
        if (typeLogic == 'label' and name not in self.labels_for_nodes.keys()) or \
            (typeLogic == 'predicate' and name not in self.predicates_for_nodes.keys()):
            print(f'\t\t\tError, the {typeLogic} {name} is not an existing {typeLogic}')
            exit()


           #

        print(f'\t\t\t\tEvaluating get_BooleanValue for  type {typeLogic}, name {name}, level {level}, domain element {domain_element}')
        ##for input symbol   {self.word[domain_element]}')


        if level == 0:
            if typeLogic == 'label':
                returnValue = self.labels_for_nodes[name].get((0,domain_element))
                print(f'\t\t\t\t\tReturning an input label value {returnValue}')
                return returnValue
            elif typeLogic == 'predicate':
                if self.predicates_for_nodes[name].get((0,domain_element)) is not None:
                    returnValue = self.predicates_for_nodes[name][(0,domain_element)]
                    print("\t\t\t\t\tThe value was already evaluated in a previous get")
                    print(f'\t\t\t\t\tReturning an input predicate value {returnValue}')
                    return returnValue
                print('\t\t\t\t\tWill evaluate the predicate using the user predicate list for: '  + str(name))
                found = self.importedModule.personal_Predicate_Formula(self, name, (0,domain_element))
                print('\t\t\t\t\tReturned predicate value for '+str(name)+' was: ' + str(found))
                if found is None:
                    print('\t\t\t\t\tThe value is None. Is this Error, because it was false before?')
                    exit()
                    self.predicates_for_nodes[name][(0,domain_element)] = False
                else:
                    self.predicates_for_nodes[name][(0,domain_element)] = found
                return found

        if level in self.copyset:
            if typeLogic == 'label':
                if self.labels_for_nodes[name].get((level,domain_element)) is not None:
                    print("\t\t\t\t\tThe value was already evaluated in a previous get")
                    return self.labels_for_nodes[name][(level,domain_element)]
                else:
                    print('\t\t\t\t\tWill evaluate the output label using the user label list for: ' + str(name))
                    found = self.importedModule.personal_OutputLabel_Formula(self,  name, (level,domain_element))
                    print('\t\t\t\t\tReturned output label value was: ' + str(found))
                    if found is None:
                        print('\t\t\t\t\tThe value is None. Is this Error, because it was false before?')
                        exit()
                        self.labels_for_nodes[name][(level,domain_element)] = False
                    else:
                        self.labels_for_nodes[name][(level,domain_element)] = found
                    return found
    def get_NodeDomain(self,node):
        print(f"\t\t\tTrying to retrieve the domain element for node {node}")
        level,domain_element = node
        if level == None and domain_element == None:
            print(f"\t\t\tThe node is  {node}, which is the empty non-existent node\n"
                  f"\t\t\tBy default, returning None"
                  f"\t\t\t TODO check if this causes errors")
            return None
        if not domain_element in self.domain_elements:
            print(f"\t\t\t\The domain element {domain_element} does not exist in the domain\n"
                  f"\t\t\tNor is it the empty output node (None,None)\n"
                  f"\t\t\tTODO not sure if such a situation can ever arise and be correct")
            exit()
        return domain_element

    def get_NodeValue(self,typeLogic,name,node):
        level,domain_element = node

        if not ( level in [0] or level in self.copyset):
            print("\t\t\tError, wrong level given to get_NodeValue. Must be 0 or a copy")
            print(f'{level}')
            exit()
        if not (typeLogic in ['function']):
            print("\t\t\tError, wrong type given to get_NodeValue. Must be 'function'")
            print(f'{typeLogic}')

            exit()
        if (typeLogic == 'function' and name not in self.functions_for_nodes.keys()) :
            print(f'\t\t\tError, the {typeLogic} {name} is not an existing {typeLogic}')
            exit()

        if level == None and domain_element == None:
            print(f"\t\t\tThe node is  {node}, which is the empty non-existent node\n"
                  f"\t\t\tBy default, we return the empty node {node} again")
            return node
        if (level,domain_element) ==   None:
            print(f"\t\t\t\tThe level and domain element {level,domain_element} is None, which means we return False by default"
                  f"TODO test break")
            exit()
            return False

        if not (domain_element == (None,None) or domain_element in self.domain_elements):
            print(f"\t\t\t\The domain element {domain_element} does not exist in the domain\n"
                  f"Nor is it the empty output node (None,None)\n"
                  f"TODO not sure if such a situation can ever arise and be correct")
            exit()
            return False
            #

        print(f'\t\t\t\tEvaluating get NodeValue for  type {typeLogic}, name {name}, level {level}, domain element {domain_element}')
        ##for input symbol   {self.word[domain_element]}')


        if level == 0:
            if typeLogic == "function":
                returnValue = self.functions_for_nodes[name].get((0,domain_element))
                print(f'\t\t\t\t\tReturning an input function value {returnValue}')
                return returnValue

        if level in self.copyset:
            if typeLogic =="function":
                if self.functions_for_nodes[name].get((level,domain_element)) is not None:
                    print("\t\t\t\t\tThe value was already evaluated in a previous get")
                    return self.functions_for_nodes[name][(level,domain_element)]
                else:
                    found = self.importedModule.personal_OutputFunction_Formula(self, name, (level, domain_element))
                    print('\t\t\t\t\tReturned output function value was: ' + str(found))
                    if found is None:
                        print('\t\t\t\t\tThe value is None. Error? It used to be set to (None,None)')
                        exit()
                        found = (None,None)
                    assert type(found) is tuple
                    if found[0] in self.copyset and found not in self.overtOutputSegments.keys():
                        print(f'\t\t\t\t\tThe value is {level,domain_element} which is not an overt output segment'
                              f'\t\t\t\t\tSo we return (None,None)')
                        found = (None,None)
                    if found[0] !=  None and  found[1] ==  None:
                        print(f'\t\t\t\t\tThe value is {found}.\n'
                              f'\t\t\t\t\tBecause the domain is non-existent, returning the empty node (Node,Node)')
                        found = (None,None)
                    self.functions_for_nodes[name][(level,domain_element)]  = found
                    return found


    def create_output_display(self):
        self.display.append(['<pred>'] * (self.domain_size + 1))
        for predicate in self.predicates_for_nodes.keys():
            line = [predicate]
            for domain_element in self.domain_elements:
                line = line + [self.predicates_for_nodes[predicate][(0, domain_element)]]
            self.display.append(line)
        self.display.append(['-'] * (self.domain_size + 1))

        for copy in self.copyset:
            self.display.append(['<'+str(copy)+'>'] * (self.domain_size + 1))
            for label in self.labels_for_nodes.keys():
                line = [label]
                for domain_element in self.domain_elements:
                    line = line + [self.labels_for_nodes[label][(copy, domain_element)]]
                self.display.append(line)
            for function in self.functions_for_nodes.keys():
                line = [function]
                for domain_element in self.domain_elements:
                    line = line + [self.functions_for_nodes[function][(copy, domain_element)]]
                self.display.append(line)
            self.display.append(['-'] * (self.domain_size + 1))

    def create_output_segments(self):
        # TODO ideally we would be using the succ/pred functions via the node list
        # but that requires picking the initial symbol in the output somehow
        print(f"Creating output segments using overt segments:\n{self.overtOutputSegments}")
        print(f"And with function list:\n{self.functions_for_nodes}")
        # if self.inputIsString:
        #     self.output_segmentsForOrderingSucc = {}
        #     self.output_segmentsForOrderingPred = {}
        for copy in self.copyset:
            listForOutputsInCopy= []
            for element in self.domain_elements:
                print(f'\tProcessing copy-element {copy,element} with overtness value {self.overtOutputSegments.get((copy,element))}')
                elementIfOvert = self.overtOutputSegments.get((copy,element))
                if not elementIfOvert == None:
                    listForOutputsInCopy.append(elementIfOvert)
                    # if self.inputIsString:
                    #     self.output_segmentsForOrderingSucc[(copy, element)] = self.functions_for_nodes['succ'][
                    #         (copy, element)]
                    #     self.output_segmentsForOrderingPred[(copy, element)] = self.functions_for_nodes['pred'][
                    #         (copy, element)]
                else:
                    listForOutputsInCopy.append('')

            self.display.append([''] + listForOutputsInCopy)

        # print(f'Created the following output segments for displaying succ:\n\t{self.output_segmentsForOrderingSucc}')
        # print(f'Created the following output segments for displaying pred:\n\t{self.output_segmentsForOrderingPred}')

    def cleanUpStringPath(self):
        if self.inputIsString and self.isOrderPreserving:
            print(f'The transduction must create a string')
            print(f'We process the transduction to remove succ/pred functions to or from non-overt output nodes'
                  f'\nIm not sure if this should be restricted to order preserving functions')
            print(f'The initial function list is:\n{self.functions_for_nodes}')
            for copy in self.copyset:
                for domain_element in self.domain_elements:
                    node = (copy,domain_element)
                    if node in self.overtOutputSegments:
                        print(f'\tNode {node} is overt so its pred/succ stay')
                    else:
                        print(f'\tNode {node} is not overt so its pred/succ must connect')
                        self.connectBetweenNodes(node)
                        print(f'Function list has changed:\n{self.functions_for_nodes}')
    def connectBetweenNodes(self,nodeB):
        # Given a node B, will connect the predecessor A to the successor C
        # Node B will lose any predecessor and successor information
        nodeA = self.functions_for_nodes['pred'][nodeB]
        nodeC = self.functions_for_nodes['succ'][nodeB]
        print(f'\tPredecessor {nodeA} and successor {nodeC}')
        if nodeA == (None,None) and nodeC == (None,None):
            print(f"\tPredecessor does not exist and the successor does not exist")

        elif nodeA == (None,None) and not nodeC == (None,None):
            print(f"\tPredecessor does not exist but successor exists")
            self.functions_for_nodes['succ'][nodeB] = (None, None)
            self.functions_for_nodes['pred'][nodeC] = (None,None)
        elif not nodeA == (None,None) and  nodeC == (None,None):
            print(f"\tPredecessor exists but successor does not exist")
            self.functions_for_nodes['succ'][nodeA] = (None,None)
            self.functions_for_nodes['pred'][nodeB] = (None,None)
        else:
            print(f"\tPredecessor exists and successor exists")
            self.functions_for_nodes['succ'][nodeA] = nodeC
            self.functions_for_nodes['pred'][nodeC] = nodeA
            self.functions_for_nodes['pred'][nodeB] = (None,None)
            self.functions_for_nodes['succ'][nodeB] = (None, None)


    def create_output_segments_String(self):
        #Goes through the list of overt nodes and their succ/pred functions to create a string
        if self.inputIsString:
            print(f'Will generate an output string')
            print(f'\tList of overt nodes:\n{self.overtOutputSegments}')
            print(f'\tList of succ functions:\n{self.functions_for_nodes["succ"]}')
            print(f'\tList of pred functions:\n{self.functions_for_nodes["pred"]}')
            startingPoint = None
            endingPoint = None

            for node in self.overtOutputSegments.keys():
                if self.functions_for_nodes['pred'][node] == (None,None):
                    if startingPoint == None:
                        startingPoint = node
                    else:
                        print(f'Error,the output includes more than one overt output segment that starts the string')
                        exit()
                if self.functions_for_nodes['succ'][node] == (None,None):
                    if endingPoint == None:
                        endingPoint = node
                    else:
                        print(f'Error,the output includes more than one overt output segment that ends the string')
                        exit()

            print(f"The string starts at {startingPoint} and ends at {endingPoint}")
            self.outputString = ''
            if startingPoint == None and endingPoint == None:
                print(f"The transduction creates the empty string")
                return
            currentpoint = startingPoint
            reachedEndPoint = False
            while not reachedEndPoint:
                if currentpoint == endingPoint:
                    reachedEndPoint = True
                currentpoint_segment = self.overtOutputSegments[currentpoint]
                self.outputString = self.outputString + currentpoint_segment
                nextpoint = self.functions_for_nodes['succ'][currentpoint]
                currentpoint = nextpoint
        else:
            print(f'TODO')
            exit()
    def print_display(self):
        print("Input and output graphs are printed into the print.message.log")
        # The printing code was taken from https://stackoverflow.com/a/2513511
        old_stdout = sys.stdout
        log_file = open(self.bmrs + ".print.message.log", "w")
        sys.stdout = log_file

        for row in self.display:
            print(*row, sep='\t')

        print(self.outputString)
        sys.stdout = old_stdout
        log_file.close()



