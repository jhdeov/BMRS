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
    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)

    if copy == 1 and label == 's': return self.get_value('input','label',label,domain_element)
    if copy == 1 and label == 'H':
        if self.get_value('input','predicate','final',domain_element):  return False
        elif self.get_value( 1,'label','H',pred):
            return True
        else: return self.get_value('input','label','H',domain_element)

def personal_Predicate_Formula(self,predicate,domain_element):

    if predicate == 'final':
        succ = self.get_value('input','function','succ',domain_element)
        if self.get_value('input','label','%',succ): return True
        else: return False

    return