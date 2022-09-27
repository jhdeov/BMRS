# Given an input string or input tree, convert the input to a word model
import sys


class word_model:
    def __init__(self,word_model_format,input_word):
        self.word_model_format=word_model_format
        self.input_word=input_word


        print(f'input_word:{self.input_word}')
        if word_model_format == 'string':
            self.create_string_word_model()
        elif word_model_format == 'tree':
            self.create_tree_word_model()
        else:
            print(f'TODO: create graph model')


    def create_string_word_model(self):
        #Assume the input string is a word like 'abc' without word boundaries
        #We add the boundaries
        # if the input word was a string like "LLL", then we turn it into a list with word boundaries
        # ["#, "L", "L", "L", "%"]
        # We do this so that we have a single representation for string inputs and feature inputs
        if type(self.input_word) is str: self.enriched_input_word = list(self.input_word)
        self.enriched_input_word=['#'] + self.enriched_input_word + ['%']
        print(f'enriched_input_word:{self.enriched_input_word}')
        self.domain_element_list = list(range(len(self.enriched_input_word)))
        print(f'domain_element_list:{self.domain_element_list}')
        self.domain_element_to_label = []
        for domain_element in self.domain_element_list:
            self.domain_element_to_label.append((domain_element,self.enriched_input_word[domain_element]))
        print(f'domain_element_to_label:{self.domain_element_to_label}')
        self.successor_functions = []
        for domain_element in self.domain_element_list[:-1]:
            self.successor_functions.append((domain_element, domain_element+1))
        print(f'successor_functions:{self.successor_functions}')
        self.predecessor_functions = []
        for successor_function  in self.successor_functions:
            self.predecessor_functions.append(tuple(reversed(successor_function)))
        print(f'predecessor_functions:{self.predecessor_functions}')

    # pushForTree and parse_bracket were adapted from https://stackoverflow.com/a/50702934
    def pushForTree(self,obj, l, depth):
        while depth:
            l = l[-1]
            depth -= 1
        # I adapted this so that characters form strings, not separate list items
        # print(f"gonna append {obj} to {l}")
        if len(l) is 0:
            l.append(obj)
        elif len(obj) is 0:
            if l[-1][-1] is " ":  # this to prevent cases like ["foo ", ['x]]
                l[-1] = l[-1].strip()
            l.append(obj)
        elif type(l[-1]) is list:
            if obj is not ' ':  # this is to prevent cases like [['x'], " "]
                l.append(obj)
        elif l[-1][-1] is " ":
            l[-1] = l[-1].strip()
            l.append(obj)
        else:
            l[-1] = l[-1] + obj
        # print(f"appended: {l}")
    def parse_bracket(self,s):
        groups = []
        depth = 0
    
        try:
            for char in s:
                if char == '[':
                    self.pushForTree([], groups, depth)
                    depth += 1
                elif char == ']':
                    depth -= 1
                else:
                    self.pushForTree(char, groups, depth)
        except IndexError:
            raise ValueError('Bracket mismatch')
    
        if depth > 0:
            raise ValueError('Bracket mismatch')
        else:
            return groups
    
        # read input
    def PreorderTraversal(self,treelist,address,tabs):
        #Traverse the tree (as a list) in pre-order so that we create the gorn addresses as domain indexes
        #print(f'{tabs}Treelist:{treelist}')
        #print(tabs+treelist[0])
        self.domain_element_list.append(address)
        self.domain_element_to_label.append((address,treelist[0]))
        for subtreelistIndex in range(1,len(treelist)):
            self.PreorderTraversal(treelist[subtreelistIndex],address+f'{subtreelistIndex-1}',tabs+'\t')
    def create_tree_word_model(self):
        # Assume the input tree is a bracketed tree like "[a [a [b] [a]] [b [a] [c]]]"
        # Note the extra initial and final []. The node labels cannot have spaces
        self.enriched_input_word =self.input_word[1:-1]
        self.parsed_tree = self.parse_bracket(self.enriched_input_word)
        print(f"parsed_tree:{self.parsed_tree}")
        self.domain_element_list = []
        self.domain_element_to_label = []
        self.PreorderTraversal(self.parsed_tree,'','')
        print(f'domain_element_list:{self.domain_element_list}')
        print(f'domain_element_to_label:{self.domain_element_to_label}')
        self.dominance_relations = []
        self.left_of_functions = []
        for domain_element in self.domain_element_list[1:]:
            self.dominance_relations.append((domain_element[:-1],domain_element))
            if int(domain_element[-1])>0:
                self.left_of_functions.append((domain_element[:-1]+str(int(domain_element[-1])-1), domain_element))
        print(f'dominance_relations:{self.dominance_relations}')
        print(f'left_of_functions:{self.left_of_functions}')
        self.mother_of_functions = []
        for dominance_relation in self.dominance_relations:
            self.mother_of_functions.append(tuple(reversed(dominance_relation)))

