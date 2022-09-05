"""Iterative epenthesis for CVC language  with right-to-left parsing
Source is AMP 2020 poster
"""

def personal_setup(self):
    self.input_symbols = list('ptkbdgmnlrszfvh') + list('aiu')
    self.labels_list = ['#', '%' ] + self.input_symbols
    self.copyset = [1,2]
    self.labels_are_input= True


def personal_predicate_setup(self):
    """Give a list of your predicates as string"""
    self.predicates_list =  ['C','V','L','R','initial','final']



def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.get_value('input', 'function', 'pred', domain_element)
    succ = self.get_value('input', 'function', 'succ', domain_element)

    if copy is 1 and label in self.input_symbols:
        return self.get_value('input', 'label', label, domain_element)

    elif copy is 2 and label == 'i':
        if self.get_value('input','predicate','C',domain_element):
            if self.get_value('input','predicate','L',domain_element):
                if self.get_value('input','predicate','C',succ): return True

def personal_Predicate_Formula(self,predicate,domain_element):
    succ = self.get_value('input', 'function', 'succ', domain_element)
    succ_of_succ = self.get_value('input', 'function', 'succ', succ)
    pred = self.get_value('input', 'function', 'pred', domain_element)

    if predicate == 'C':
        for label in list('ptkbdgmnlrszfvh'):
            if self.get_value('input','label',label,domain_element): return True
    elif predicate == 'V':
        for label in list('aiu'):
            if self.get_value('input','label',label,domain_element): return True
    elif predicate == 'initial':
        if self.get_value('input','label','#',pred): return True
    elif predicate == 'final':
        if self.get_value('input','label','%',succ): return True


    #I follow the definition in  AMP poster (canceled Sigmorphon paper)
    elif predicate == 'L':
        #selects a consonant which precedes a vowel
        if self.get_value('input','predicate','C',domain_element) \
            and self.get_value('input','predicate','V',succ): return True
        #selects a word-initial vowe
        if self.get_value('input','predicate','V',domain_element) \
            and self.get_value('input','predicate','initial',domain_element): return True
        #selects a consonant which precedes a consonantwhich precedes the left edge of a syllable
        if self.get_value('input','predicate','C',domain_element) \
            and self.get_value('input','predicate','C',succ) \
            and self.get_value('input','predicate','L',succ_of_succ): return True
        #selects a word-initial consonant which precedes a syllable boundary
        if self.get_value('input','predicate','C',domain_element) \
            and self.get_value('input','predicate','initial',domain_element) \
            and self.get_value('input','predicate','L',succ) : return True
        #selects a consonant which precedes a word-final consonant
        if self.get_value('input', 'predicate', 'C', domain_element) \
                and self.get_value('input', 'predicate', 'C', succ) \
                and self.get_value('input', 'predicate', 'final', succ): return True

        else: return False


