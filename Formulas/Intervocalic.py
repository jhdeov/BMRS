"""Intervocalic voicing of consonants"""

def personal_setup(self):
    self.input_symbols=['p','t','k','b','d','g','a','i','u']
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
    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)

    if copy == 1 and label == 'voiced':
        pred = self.get_value('input','function','pred',domain_element)
        succ = self.get_value('input','function','succ',domain_element)
        if self.get_value('input','label','vowel',pred) and self.input_to_labels['vowel'].get(succ) and \
            self.get_value('input','label','consonant',domain_element):
            return True
        else:
            return self.get_value('input','label','voiced',domain_element)
    if copy == 1 and label in self.labels_list and label != 'voiced':
        return self.get_value('input','label',label,domain_element)

def personal_Predicate_Formula(self,predicate,domain_element):
    return