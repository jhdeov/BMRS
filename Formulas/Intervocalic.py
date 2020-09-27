"""Intervocalic voicing of consonants"""

def personal_setup(self):
    self.labels_list = ['voiced', 'labial', 'coronal', 'dorsal', 'low', 'high', 'front', 'back', 'consonant', 'vowel',
                        '#', '%']
    self.copyset = [1]
    self.labels_are_input=False



def personal_features(self):
    self.symbol_to_labels = {
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
    return

def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)

    if copy == 1 and label == 'voiced':
        pred = self.input_to_functions['pred'].get(domain_element)
        succ = self.input_to_functions['succ'].get(domain_element)
        if self.input_to_labels['vowel'].get(pred) and self.input_to_labels['vowel'].get(succ) and \
            self.input_to_labels['consonant'].get(domain_element):
            return True
        else:
            return self.input_to_labels['voiced'].get(domain_element)
    if copy == 1 and label in self.labels_list and label != 'voiced':
        return self.input_to_labels[label].get(domain_element)

def personal_Predicate_Formula(self,predicate,domain_element):
    return