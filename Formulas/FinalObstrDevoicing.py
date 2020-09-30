"""Final devoicing of obstruents
Restricted alphabet of [p,t,n,e]
"""

def personal_setup(self):
    self.input_symbols = list('tend')
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
    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)


    if copy == 1 and label == 'voiced':
        if self.get_value('input','predicate','final voiced obstruent',domain_element): return False
        else: return self.get_value('input','label','voiced',domain_element)
    if copy == 1 and label in ['vowel','sonorant','consonant']:
        return self.get_value('input','label',label,domain_element)

def personal_Predicate_Formula(self,predicate,domain_element):
    if predicate == 'voiced obstruent':
        if self.get_value('input','label','sonorant',domain_element): return False
        else: return self.get_value('input','label','voiced',domain_element)
    if predicate == 'final':
        succ = self.get_value('input','function','succ',domain_element)
        if self.get_value('input','label','%',succ): return True
        else: return False
    if predicate == 'final voiced obstruent':
        if self.get_value('input','predicate','voiced obstruent',domain_element):
            return self.get_value('input','predicate','final',domain_element)
        else: return False
