"""Testing out what deletion of a symbol 'b' looks like
"""

def personal_setup(self):
    """Make sure that you include the symbols # and % in your list of labels"""
    self.labels_list = ['#', '%', ] + list('abc')

    self.input_symbols = list('abc')

    self.copyset = [1]

    self.labels_are_input=  True


def personal_features(self):
    return

def personal_predicate_setup(self):
    return

def personal_Output_Formula(self, copy, label, domain_element):


    if copy == 1 and label == 'a':
        if self.get_value('input', 'label', 'a', domain_element): return True
        else: return False
    if copy == 1 and label == 'c':
        if self.get_value('input', 'label', 'c', domain_element): return True
        else: return False


def personal_Predicate_Formula(self,predicate,domain_element):
    return