"""Iterative stress with heavy and light syllables
input strings can only be L's and H's
"""

def personal_setup(self):
    self.labels_list = ['#', '%', 'H', 'L','stress']
    self.copyset = [1]
    self.labels_are_input=False



def personal_features(self):
    self.symbol_to_labels = {
        'H': frozenset(['H']),
        'L': frozenset(['L']),
        'H\'': frozenset(['H','stress']),
        'L\'': frozenset(['L','stress']),
        '#': frozenset(['#']),
        '%': frozenset(['%'])
    }
    self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}

def personal_predicate_setup(self):
    self.predicates_list = ['initial','final','syll','clash','lapse','only']



def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)



    if copy is 1 and label == 'stress':
        if self.get_predicate_value('only',domain_element): return True
        elif self.get_predicate_value('final',domain_element): return False
        elif self.input_to_labels['H'].get(domain_element): return True
        elif self.get_predicate_value('initial',domain_element):return False
        elif self.get_predicate_value('clash',domain_element): return False
        else: return self.get_predicate_value('lapse',domain_element)
    if copy == 1 and label == 'H':
        if self.get_output_value(1, 'stress', domain_element): return True
        else: return self.input_to_labels['H'].get(domain_element)
    if copy == 1 and label == 'L':
        if self.get_output_value(1, 'stress', domain_element): return False
        else: return self.input_to_labels['L'].get(domain_element)


def personal_Predicate_Formula(self,predicate,domain_element):
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)

    if predicate == 'final':
        if self.input_to_labels['%'].get(succ): return True
        else: return False
    if predicate == 'initial':
        if self.input_to_labels['%'].get(pred): return True
        else: return False
    if predicate == 'syll':
        if self.input_to_labels['L'].get(domain_element): return True
        else:
            return self.input_to_labels['H'].get(domain_element)
    if predicate == 'clash':
        if self.get_predicate_value('syll', domain_element):
            return self.get_output_value(1, 'stress', pred)
        else:
            return False
    if predicate == 'lapse':
        if self.get_output_value(1,'stress',pred): return False
        else:
            if self.get_predicate_value('syll',pred): return self.get_predicate_value('syll',domain_element)
            else: return False
    if predicate == 'only':
        if self.get_predicate_value('final',domain_element):
            return self.get_predicate_value('initial',domain_element)
        else:
            if self.get_predicate_value('final',succ):
                return self.get_predicate_value('initial',domain_element)
            else: return False