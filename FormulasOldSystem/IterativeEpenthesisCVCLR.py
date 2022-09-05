"""Iterative epenthesis for CVC language with left-to-right parsing
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
        if self.get_value('input','predicate','C',domain_element) \
            and self.get_value('input','predicate','C',succ) \
            and self.get_value('input','predicate','R',succ) \
            and not self.get_value('input','predicate','final',succ): return True #\
            #and not self.get_value('input','predicate','final',succ) : return True
            # this will add a schwa between ..bb...
            #the negation  prevents /babb/-->//bab.b//--> *bab.ib instead of bab.bi;
            #   could reforumulate this last conjunct as --R(x)
        if self.get_value('input','predicate','C',domain_element) \
            and self.get_value('input','predicate','R',domain_element) \
            and self.get_value('input', 'predicate', 'final', domain_element) \
            and self.get_value('input', 'predicate', 'R', pred): return True
            #(this is just for the context /....ab.b/-->[...b.bi]
        if self.get_value('input', 'predicate', 'C', domain_element) \
                and self.get_value('input', 'predicate', 'final', succ) \
                and self.get_value('input', 'predicate', 'C', succ) \
                and self.get_value('input', 'predicate', 'R', pred): return True
        # (this is just for the context /....ab.bb/-->[...b.bi]


def personal_Predicate_Formula(self,predicate,domain_element):
    succ = self.get_value('input', 'function', 'succ', domain_element)
    succ_of_succ = self.get_value('input', 'function', 'succ', succ)
    pred = self.get_value('input', 'function', 'pred', domain_element)
    pred_of_pred = self.get_value('input', 'function', 'pred', pred)

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
    elif predicate == 'R':
        #select a final segment, every word ends in a syllable
        if self.get_value('input','predicate','final',domain_element): return True
        #selects a consonant after a vowel, so it'll give the weird selection /aba/->//ab.a//)
        if self.get_value('input','predicate','C',domain_element) \
            and self.get_value('input','predicate','V',pred): return True
        #selects the second C in /bba/-->//bib.a// and /bbba/-->bib.ba
        if self.get_value('input','predicate','C',domain_element) \
            and self.get_value('input','predicate','C',pred) \
            and self.get_value('input','predicate','initial',pred) : return True
        #selects the   third C in /abbba/-->//ab.bib.a//  and
        # /abbbba/-->ab.bib.ba and fourth Cin /bbbba/->//bib.bib.a//,/bbbbba/-->bib.bib.ba
        if self.get_value('input','predicate','C',domain_element) \
            and self.get_value('input','predicate','C',pred) \
            and self.get_value('input','predicate','R',pred_of_pred) : return True
