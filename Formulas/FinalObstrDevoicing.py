"""Final devoicing of obstruents
Restricted alphabet of [p,t,n,e]
"""

def personal_setup(self):
    self.labels_list = ['#', '%', 'voiced', 'consonant', 'sonorant','vowel']
    self.copyset = [1]
    self.labels_are_input=False



def personal_features(self):
    self.symbol_to_labels = {
        't': frozenset(['consonant']),
        'd': frozenset(['consonant', 'voiced']),
        'n': frozenset(['sonorant']),
        'e': frozenset(['sonorant','vowel']),
        '#': frozenset(['#']),
        '%': frozenset(['%'])
    }
    self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}

def personal_predicate_setup(self):
    self.predicates_list = ['voiced obstruent', 'final','final voiced obstruent']


def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)


    if copy == 1 and label == 'voiced':
        if self.get_predicate_value('final voiced obstruent',domain_element): return False
        else: return self.input_to_labels['voiced'].get(domain_element)
    if copy == 1 and label in ['vowel','sonorant','consonant']:
        return self.input_to_labels[label].get(domain_element)

def personal_Predicate_Formula(self,predicate,domain_element):
    if predicate == 'voiced obstruent':
        if self.input_to_labels['sonorant'].get(domain_element): return False
        else: return self.input_to_labels['voiced'].get(domain_element)
    if predicate == 'final':
        succ = self.input_to_functions['succ'].get(domain_element)
        if self.input_to_labels['%'].get(succ): return True
        else: return False
    if predicate == 'final voiced obstruent':
        if self.get_predicate_value('voiced obstruent',domain_element):
            return self.get_predicate_value('final',domain_element)
        else: return False
