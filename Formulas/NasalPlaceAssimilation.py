"""Nasal place assimilation
Doesn't work because a nasal doesnt lose any of its underlying places
"""

def personal_setup(self):
    self.input_symbols = list('ptkbdgmnNaiu')
    self.labels_list = ['#', '%', 'voiced', 'labial', 'coronal', 'dorsal', 'low', 'high', 'front', 'back', 'consonant', 'vowel',
                        'nasal']
    self.copyset = [1]
    self.labels_are_input=False




def personal_features(self):
    self.symbol_to_labels = {
        'm': frozenset(['consonant', 'labial','nasal','voiced']),
        'n': frozenset(['consonant', 'coronal','nasal','voiced']),
        'N': frozenset(['consonant', 'dorsal','nasal','voiced']),
        'p': frozenset(['consonant', 'labial']),
        't': frozenset(['consonant', 'coronal']),
        'k': frozenset(['consonant', 'dorsal']),
        'b': frozenset(['consonant', 'labial', 'voiced']),
        'd': frozenset(['consonant', 'coronal', 'voiced']),
        'g': frozenset(['consonant', 'dorsal', 'voiced']),
        'a': frozenset(['vowel', 'low', 'back', 'voiced']),
        'i': frozenset(['vowel', 'high', 'front', 'voiced']),
        'u': frozenset(['vowel', 'high', 'back', 'voiced']),
        '#': frozenset(['#']),
        '%': frozenset(['%'])
    }
    self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}

def personal_predicate_setup(self):
    self.predicates_list = ['prelabial nasal', 'precoronal nasal', 'predorsal nasal']



def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)

    if copy == 1 and label == 'labial':
        if self.get_predicate_value('prelabial nasal',domain_element): return True
        else: return self.input_to_labels['labial'].get(domain_element)
    if copy == 1 and label == 'coronal':
        if self.get_predicate_value('precoronal nasal',domain_element):
            return True
        else:
            return self.input_to_labels['coronal'].get(domain_element)
    if copy == 1 and label == 'dorsal':
        if self.get_predicate_value('predorsal nasal',domain_element): return True
        else: return self.input_to_labels['dorsal'].get(domain_element)

    if copy == 1 and label not in ['labial','coronal','dorsal']:
        return self.input_to_labels[label].get(domain_element)


def personal_Predicate_Formula(self,predicate,domain_element):
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)

    print('h')
    if predicate == 'prelabial nasal':
        print('hi')
        if self.input_to_labels['nasal'].get(domain_element):
            return self.input_to_labels['labial'].get(succ)
        else: return False
    if predicate == 'precoronal nasal':
        if self.input_to_labels['nasal'].get(domain_element):
            return self.input_to_labels['coronal'].get(succ)
        else: return False
    if predicate == 'predorsal nasal':
        if self.input_to_labels['nasal'].get(domain_element):
            return self.input_to_labels['dorsal'].get(succ)
        else: return False

