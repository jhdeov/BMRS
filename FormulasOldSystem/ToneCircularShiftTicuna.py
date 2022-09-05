"""Tone shift in Ticuna, based on Oakden (ms.) "The Ticuna nominalizer tone circle and input strict-locality"
"""

def personal_setup(self):
    self.input_symbols = ['#r','N', #root-initial boundary and the nominalizer
                          '1','2','3','4','5'
                          '31', '43', '51'
                          '1c'      #creaky1
                          ]
    self.labels_list = ['#', '%' ] + self.input_symbols
    self.copyset = [1]
    self.labels_are_input= True

def personal_features(self):
    self.symbol_to_labels = {
        '#': frozenset(['#']),
        '%': frozenset(['%']),
        "REPLACE ME": frozenset([ "REPLACE ME"]),
    #Example:
    #    'p': frozenset(['labial', 'consonant']),
     #   'L\'': frozenset(['L', 'stress']),

    }
    self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}

def personal_predicate_setup(self):
    """Give a list of your predicates as string"""
    self.predicates_list =  ['s',                       #s is syllable
                             '#r_4_N', 's_3_N', '_1_N',  #_x_ indicates that x is the domain element in question
                             '#r_3_N',
                             '_1_N', '#r_31_N', '_3_N',
                             '_1c_N', 's_4_N',
                             '#r_43_N', '#r_31_N',
                             '1(c)',                  #syllabic tone symbols of either tone 1 or 1-creaky 
                             '#r_1c_1(c)'
                             ]




def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.get_value('input', 'function', 'pred', domain_element)
    succ = self.get_value('input', 'function', 'succ', domain_element)

    if copy is 1 and label == '1':
        if self.get_value('input','predicate','#r_4_N',domain_element): return True
        elif self.get_value('input', 'predicate', 's_3_N', domain_element): return True
        elif self.get_value('input','predicate','_1_N',domain_element): return False
        else: return self.get_value('input','label','1',domain_element)
    if copy is 1 and label == '2':
        if self.get_value('input','predicate','#r_3_N',domain_element): return True
        else: return self.get_value('input','label','2',domain_element)
    if copy is 1 and label == '3':
        if self.get_value('input','predicate','_1_N',domain_element): return True
        elif self.get_value('input', 'predicate', '#r_31_N', domain_element): return True
        elif self.get_value('input','predicate','_3_N',domain_element): return False
        else: return self.get_value('input','label','3',domain_element)
    if copy is 1 and label == '1c':
        if self.get_value('input','predicate','#r_1c_1(c)',domain_element): return False
        else: return self.get_value('input','label','1c',domain_element)
    if copy is 1 and label == '5':
        if self.get_value('input','predicate','_1c_N',domain_element): return True
        elif self.get_value('input', 'predicate', 's_4_N', domain_element): return True
        elif self.get_value('input','predicate','#r_1c_1(c)',domain_element): return True
        else: return self.get_value('input','label','5',domain_element)
    if copy is 1 and label == '31':
        if self.get_value('input','predicate','#r_43_N',domain_element): return True
        elif self.get_value('input', 'predicate', '#r_31_N', domain_element): return False
        else: return self.get_value('input','label','31',domain_element)
    if copy is 1 and label == '51':
        return self.get_value('input', 'label', '51', domain_element)

    #Missing output functions for 43 and 4

def personal_Predicate_Formula(self,predicate,domain_element):
    pred = self.get_value('input', 'function', 'pred', domain_element)

    succ = self.get_value('input','function','succ',domain_element)

    if predicate == 's':
        if self.get_value('input','input','#r',domain_element): return False
        elif self.get_value('input','label','N',domain_element): return False
        else: return True
    if predicate == '1(c)':
        if self.get_value('input','label','s',domain_element):
            if self.get_value('input','label','1',domain_element): return True
            elif  self.get_value('input','label','1c',domain_element): return True
            else: return False
        else: return False


    #I have to turn your local contexs into predicates
    #If there's no 'else' value, then the code automatically interprets the None as False
    
    if predicate == '#r_4_N':
        if self.get_value('input', 'input', '#r', pred):
            if self.get_value('input', 'label', '4', domain_element):
                if self.get_value('input', 'label', 'N', succ): return True
    if predicate == '#r_3_N':
        if self.get_value('input', 'label', '#r', pred):
            if self.get_value('input', 'label', '3', domain_element):
                if self.get_value('input', 'label', 'N', succ): return True
    if predicate == '#r_31_N':
        if self.get_value('input', 'label', '#r', pred):
            if self.get_value('input', 'label', '31', domain_element):
                if self.get_value('input', 'label', 'N', succ): return True
    if predicate == 's_3_N':
        if self.get_value('input', 'predicate', 's', pred):
            if self.get_value('input', 'label', '3', domain_element):
                if self.get_value('input', 'label', 'N', succ): return True
    if predicate == 's_4_N':
        if self.get_value('input', 'predicate', 's', pred):
            if self.get_value('input', 'label', '4', domain_element):
                if self.get_value('input', 'label', 'N', succ): return True
    if predicate == '#r_43_N':
        if self.get_value('input', 'label', '#r', pred):
            if self.get_value('input', 'label', '43', domain_element):
                if self.get_value('input', 'label', 'N', succ): return True

    if predicate == '_1_N':
        if self.get_value('input', 'label', '1', domain_element):
           if self.get_value('input', 'label', 'N', succ): return True
    if predicate == '_3_N':
        if self.get_value('input', 'label', '3', domain_element):
           if self.get_value('input', 'label', 'N', succ): return True
    if predicate == '_1c_N':
        if self.get_value('input', 'label', '1c', domain_element):
           if self.get_value('input', 'label', 'N', succ): return True

    if predicate == '#r_1c_1(c)':
        if self.get_value('input', 'label', '#r', pred):
            if self.get_value('input','label','1c',domain_element):
                if self.get_value('input','predicate','1(c)',succ): return True
