"""High tone spreads from syllable all the way to the penultimate syllable
Taken from Jane-Adam paper, example 2
"""

def personal_setup(self):
    self.labels_list = list('sH#%')
    self.copyset = [1]
    self.labels_are_input=False




def personal_features(self):
       self.symbol_to_labels = {
            's': frozenset(['s']),
            'H': frozenset(['s','H']),
            '#': frozenset(['#']),
            '%': frozenset(['%']),
        }
       self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}

def personal_predicate_setup(self):
    self.predicates_list=['final']

def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)

    if copy == 1 and label == 's': return self.input_to_labels[label].get(domain_element)
    if copy == 1 and label == 'H':
        if self.get_predicate_value('final',domain_element):  return False
        elif self.get_output_value(1,'H',pred):
            return True
        else: return self.input_to_labels['H'].get(domain_element)

def personal_Predicate_Formula(self,predicate,domain_element):

    if predicate == 'final':
        succ = self.input_to_functions['succ'].get(domain_element)
        if self.input_to_labels['%'].get(succ): return True
        else: return False

    return