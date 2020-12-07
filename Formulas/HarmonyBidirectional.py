"""Based off of Heinz 2018 "Computational nature of phonological generalizations"
Bidirectional harmony: the + feature spreads in both directions
Opaque vowel doesn't it's own negative spread
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
    self.predicates_list =  ['before +','after +','before -','after +','before opaque B','after opaque B']

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
        for harmonic in ['+','-']:
            if self.get_value('input','label',harmonic,domain_element):
                if self.get_value('input', 'predicate', 'before +', domain_element): return True
                elif self.get_value('input', 'predicate', 'after +', domain_element): return True
        else: return self.get_value('input','label','+',domain_element)
    if copy is 1 and label == '-':
        for harmonic in ['+','-']:
            if self.get_value('input','label',harmonic,domain_element):
                if self.get_value('input', 'predicate', 'before +', domain_element): return False
                elif self.get_value('input', 'predicate', 'after +', domain_element): return False
        else: return self.get_value('input','label','-',domain_element)


def personal_Predicate_Formula(self,predicate,domain_element):
    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)


    if predicate == "before opaque B":
        if self.get_value('input','label','B',succ): return True
        for nonopaque in ['-','C','T']:
            if self.get_value('input','label',nonopaque,succ):
                if self.get_value('input','predicate','before opaque B',succ): return True
        else: return False
    if predicate == "after opaque B":
        if self.get_value('input','label','B',pred): return True
        for nonopaque in ['-','C','T']:
            if self.get_value('input','label',nonopaque,pred):
                if self.get_value('input','predicate','after opaque B',pred): return True
        else: return False

    if predicate == "after +":
        if self.get_value('input','label','+',pred): return True
        for nonopaque in ['-','C','T']:
            if self.get_value('input','label',nonopaque,pred):
                if self.get_value('input','predicate','after +',pred): return True
        else: return False
    if predicate == "before +":
        if self.get_value('input','label','+',succ): return True
        for nonopaque in ['-','C','T']:
            if self.get_value('input','label',nonopaque,succ):
                if self.get_value('input','predicate','before +',succ): return True
        else: return False
