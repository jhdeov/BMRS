"""Iterative epenthesis for CVC language  with left-to-right parsing
Source is AMP 2020 proceedings
"""

def personal_setup(self):
    self.input_symbols = list('ptkbdgmnlrszfvh') + list('aiu')
    self.labels_list = ['#', '%' ] + self.input_symbols + ["onset","nucleus","coda"]
    self.copyset = [1,2]
    self.labels_are_input= False

def personal_features(self):
    #Output syllable roles as subscripts.
    #Treat C and V as predicates, not input labels for convenience
    self.symbol_to_labels={
        '#': frozenset(['#']),
        '%': frozenset(['%'])
    }
    for segment in self.input_symbols:
        self.symbol_to_labels[segment]=frozenset([segment])
        self.symbol_to_labels[segment + "_o"] = frozenset([segment, "onset"])
        self.symbol_to_labels[segment + "_n"] = frozenset([segment, "nucleus"])
        self.symbol_to_labels[segment + "_c"] = frozenset([segment, "coda"])
    self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}


def personal_predicate_setup(self):
    """Give a list of your predicates as string"""
    self.predicates_list =  ['C','V','initial','final']



def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.get_value('input', 'function', 'pred', domain_element)
    succ = self.get_value('input', 'function', 'succ', domain_element)
    pred_of_pred = self.get_value('input', 'function', 'pred', pred)

    #Output segments
    if copy is 1 and label in self.input_symbols:
        return self.get_value('input', 'label', label, domain_element)
    # Output vowels as nuclei
    if copy is 1 and label == "nucleus":
        return self.get_value('input', 'predicate', "V", domain_element)

    #Recursively generate codas
    if copy is 1 and label == "coda":
        if self.get_value('input', 'predicate', "C", domain_element):
            if self.get_value('input', 'predicate', "final", domain_element): return True
            elif self.get_value('input', 'predicate', "V", pred):
                if self.get_value('input', 'predicate', "C", succ): return True
            elif self.get_value('input', 'predicate', "C", pred):
                if self.get_value(1, 'label', "coda", pred_of_pred):
                    if self.get_value("input", 'predicate', "C", succ): return True
        else: return False
    #Generate onsets based on codas
    if copy is 1 and label == "onset":
        if self.get_value('input', 'predicate', "C", domain_element):
            if not self.get_value(1, 'label', "coda", domain_element):
                if self.get_value('input', 'predicate', "V", succ): return True
                elif self.get_value(1, 'label', "coda", pred): return True
        else: return False

    elif copy is 2 and label == 'i':
        if self.get_value(1,'label','onset',domain_element):
            if not self.get_value(1,"label",'nucleus',succ):  return True
        else: return False

def personal_Predicate_Formula(self,predicate,domain_element):
    succ = self.get_value('input', 'function', 'succ', domain_element)
    succ_of_succ = self.get_value('input', 'function', 'succ', succ)
    pred = self.get_value('input', 'function', 'pred', domain_element)

    if predicate == 'C':
        for label in list('ptkbdgmnlrszfvh'):
            if self.get_value('input','label',label,domain_element): return True
    elif predicate == 'V':
        for label in list('aiu'):
            if self.get_value('input','label',label,domain_element): return True
    elif predicate == 'initial':
        if self.get_value('input','label','#',pred): return True
    elif predicate == 'final':
        if self.get_value('input','label','%',succ): return True


