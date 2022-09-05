"""Based off of Heinz 2018 "Computational nature of phonological generalizations"
Sour grapes harmony: the first vowel's feature spreads
+ feature speread  if there's a B later in the word
In a sequence +-+B, the first - is harmonized
- fetaure spread is not blocked
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
    self.predicates_list =  ['initial', 'initial C span', 'first +', 'first -', 'after first +', 'after first -','after opaque B','before opaque B']

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
        if self.get_value('input', 'predicate', 'first +', domain_element): return True
        elif self.get_value('input', 'label', '+', domain_element):
            if self.get_value('input', 'predicate', 'after first +', domain_element): return True
            elif self.get_value('input', 'predicate', 'after first -', domain_element): return False
            elif self.get_value('input','predicate','after opaque B',domain_element): return False
        elif self.get_value('input', 'label', '-', domain_element):
            if self.get_value('input', 'predicate', 'after first -', domain_element): return False
            elif self.get_value('input', 'predicate', 'after opaque B', domain_element): return False
            elif self.get_value('input', 'predicate', 'after first +', domain_element):
                if self.get_value('input', 'predicate', 'before opaque B', domain_element): return False
                else: return True

    if copy is 1 and label == '-':
        if self.get_value('input', 'predicate', 'first -', domain_element): return True
        elif self.get_value('input', 'label', '+', domain_element):
            if self.get_value('input', 'predicate', 'after first -', domain_element): return True
            elif self.get_value('input','predicate','after opaque B',domain_element): return True
            elif self.get_value('input', 'predicate', 'after first +', domain_element): return False
            else: return False
        elif self.get_value('input', 'label', '-', domain_element):
            if self.get_value('input', 'predicate', 'after first -', domain_element): return True
            elif self.get_value('input', 'predicate', 'after opaque B', domain_element): return True
            elif self.get_value('input', 'predicate', 'after first +', domain_element):
                if self.get_value('input', 'predicate', 'before opaque B', domain_element): return True
                else: return False


def personal_Predicate_Formula(self,predicate,domain_element):
    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)

    if predicate == 'initial':
        if self.get_value('input', 'label', '#', pred): return True
        else: return False
    if predicate == 'initial C span':
        if self.get_value('input','label','C',domain_element):
            if self.get_value('input','predicate','initial',domain_element): return True
            elif self.get_value('input','predicate','initial C span',pred): return True
            else: return False
    if predicate == 'first +':
        if self.get_value('input', 'label', '+', domain_element):
            if self.get_value('input', 'predicate', 'initial', domain_element): return True
            elif self.get_value('input', 'predicate', 'initial C span', pred): return True
            else: return False
    if predicate == 'first -':
        if self.get_value('input', 'label', '-', domain_element):
            if self.get_value('input', 'predicate', 'initial', domain_element): return True
            elif self.get_value('input', 'predicate', 'initial C span', pred): return True
            else: return False

    if predicate == 'after first +':
        if self.get_value('input','predicate','first +', pred): return True
        elif self.get_value('input', 'label', 'B', pred): return False
        elif self.get_value('input', 'predicate', 'after first +', pred): return True
        else: return False

    if predicate == 'after first -':
        if self.get_value('input','predicate','first -', pred): return True
        elif self.get_value('input', 'label', 'B', pred): return False
        elif self.get_value('input', 'predicate', 'after first -', pred): return True
        else: return False
    if predicate == 'after opaque B':
        if self.get_value('input','label','B', pred): return True
        elif self.get_value('input', 'predicate', 'after opaque B', pred): return True
        else: return False

    if predicate == 'before opaque B':
        print('hi')
        if self.get_value('input','label','B', succ): return True
        elif self.get_value('input','label','+', succ): return False
        elif self.get_value('input', 'predicate', 'before opaque B', succ): return True
        else: return False

