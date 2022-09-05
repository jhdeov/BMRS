"""Based off of Meinhardt et al's 2020 manuscript "On the proper treatment of weak determinism"
Bidirectional harmony: the + feature spreads in both directions
/a/ is opaque to leftwards spread. It blocks leftward spread but does not trigger - spread
/a/ does not block rightwards spread but surfaces as [o] after +
Underlying value:
positive harmonic feature: +
negative harmonic feature: -
transparent negative harmonic feature: T
irrelevant consonant: C
I have to add /a/ and /o/ as input labels, even though there are no underlying /o/
"""

def personal_setup(self):
    """List what characters you accept as part of your input string;
     individual features inside a feature bundle are fine"""
    self.input_symbols = ['+','-','T','a','o', 'C']
    self.labels_list = ['#', '%' ] +   self.input_symbols
    self.copyset = [1]
    self.labels_are_input= True

def personal_predicate_setup(self):
    """Give a list of your predicates as string"""
    self.predicates_list =  ['before +','after +','before opaque a','after opaque a']

def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.get_value('input', 'function', 'pred', domain_element)
    succ = self.get_value('input', 'function', 'succ', domain_element)

    if copy is 1 and label =='C':
        if self.get_value('input', 'label', 'C', domain_element): return True
        else: return False
    if copy is 1 and label =='T':
        if self.get_value('input', 'label', 'T', domain_element): return True
        else: return False
    if copy is 1 and label == '+':
        if self.get_value('input','label','+',domain_element): return True
        if self.get_value('input','label','-',domain_element):
            if self.get_value('input','predicate','before +',domain_element): return True
            elif self.get_value('input','predicate','after +',domain_element): return True
    if copy is 1 and label == '-':
        if self.get_value('input','label','-',domain_element):
            if self.get_value(1,'label','+',domain_element): return False
            else: return True
    if copy is 1 and label == 'o':
        if self.get_value('input','label','a',domain_element):
            if self.get_value('input','predicate','after +',domain_element): return True
            else: return False
    if copy is 1 and label == 'a':
        if self.get_value('input','label','a',domain_element):
            if self.get_value(1,'label','o',domain_element): return False
            else: return True

def personal_Predicate_Formula(self,predicate,domain_element):
    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)


    if predicate == "before opaque a":
        if self.get_value('input','label','a',succ): return True
        for nonopaque in ['-','C','T']:
            if self.get_value('input','label',nonopaque,succ):
                if self.get_value('input','predicate','before opaque a',succ): return True
        else: return False
    if predicate == "after opaque a":
        if self.get_value('input','label','a',pred): return True
        for nonopaque in ['-','C','T']:
            if self.get_value('input','label',nonopaque,pred):
                if self.get_value('input','predicate','after opaque a',pred): return True
        else: return False

    if predicate == "after +":
        if self.get_value('input','label','+',pred): return True
        for nonopaque in ['-','a','C','T']:
            if self.get_value('input','label',nonopaque,pred):
                if self.get_value('input','predicate','after +',pred): return True
        else: return False
    if predicate == "before +":
        if self.get_value('input','label','+',succ): return True
        for nonopaque in ['-','C','T']:
            if self.get_value('input','label',nonopaque,succ):
                if self.get_value('input','predicate','before +',succ): return True
        else: return False
