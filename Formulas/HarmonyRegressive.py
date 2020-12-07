"""Based off of Heinz 2018 "Computational nature of phonological generalizations"
Regressive harmony: the last vowel's feature spreads
Opaque vowel starts it's own negative spread
Underlying value:
positive harmonic feature: +
negative harmonic feature: -
transparent negative harmonic feature: T
opaque negative harmonic feature: B
irrelevant consonant: C
"""

def personal_setup(self):
    """List what characters you accept as part of your input string;
     individual features inside a feature bundle are fine"""
    self.input_symbols = ['+','-','T','B', 'C']
    self.labels_list = ['#', '%' ] +   self.input_symbols
    self.copyset = [1]
    self.labels_are_input= True

def personal_predicate_setup(self):
    """Give a list of your predicates as string"""
    self.predicates_list =  ['final', 'final C span', 'last +', 'last -', 'before last +', 'before last -','before opaque B']

def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.get_value('input', 'function', 'pred', domain_element)
    succ = self.get_value('input', 'function', 'succ', domain_element)

    if copy is 1 and label =='C':
        if self.get_value('input', 'label', 'C', domain_element): return True
        else: return False
    if copy is 1 and label =='B':
        if self.get_value('input', 'label', 'B', domain_element): return True
        else: return False
    if copy is 1 and label =='T':
        if self.get_value('input', 'label', 'T', domain_element): return True
        else: return False
    if copy is 1 and label == '+':
        if self.get_value('input', 'predicate', 'last +', domain_element): return True
        else:
            for nonopaque in ['+','-']:
                if self.get_value('input','label',nonopaque,domain_element):
                    if self.get_value('input', 'predicate', 'before last +', domain_element): return True
            else: return False
    if copy is 1 and label == '-':
        if self.get_value('input', 'predicate', 'last -', domain_element): return True
        else:
            for nonopaque in ['+','-']:
                if self.get_value('input','label',nonopaque,domain_element):
                    if self.get_value('input', 'predicate', 'before last -', domain_element): return True
                    if self.get_value('input','predicate','before opaque B',domain_element): return True
            else: return False

def personal_Predicate_Formula(self,predicate,domain_element):
    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)

    if predicate == 'final':
        if self.get_value('input', 'label', '%', succ): return True
        else: return False
    if predicate == 'final C span':
        if self.get_value('input','label','C',domain_element):
            if self.get_value('input','predicate','final',domain_element): return True
            elif self.get_value('input','predicate','final C span',succ): return True
            else: return False
    if predicate == 'last +':
        if self.get_value('input', 'label', '+', domain_element):
            if self.get_value('input', 'predicate', 'final', domain_element): return True
            elif self.get_value('input', 'predicate', 'final C span', succ): return True
            else: return False
    if predicate == 'last -':
        if self.get_value('input', 'label', '-', domain_element):
            if self.get_value('input', 'predicate', 'final', domain_element): return True
            elif self.get_value('input', 'predicate', 'final C span', succ): return True
            else: return False

    if predicate == 'before last +':
        if self.get_value('input','predicate','last +', succ): return True
        elif self.get_value('input', 'label', 'B', succ): return False
        elif self.get_value('input', 'predicate', 'before last +', succ): return True
        else: return False

    if predicate == 'before last -':
        if self.get_value('input','predicate','last -', succ): return True
        elif self.get_value('input', 'label', 'B', succ): return False
        elif self.get_value('input', 'predicate', 'before last -', succ): return True
        else: return False

    if predicate == 'before opaque B':
        if self.get_value('input','label','B', succ): return True
        elif self.get_value('input', 'predicate', 'before opaque B', succ): return True
        else: return False

