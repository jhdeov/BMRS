"""Here's a template
Replace TO DO with your own code
"""

def personal_setup(self):

    self.input_symbols = ['+',
                        'a', 'e', 'i', 'o', 'u',
                        'b', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'z',
                        '[nom]', '[gen]', '[dat]', '[acc]', '[voc]', '[ins]', '[loc]', '[sg]', '[pl]']
    self.labels_list = self.input_symbols + ['#', '%' ]

    #Need to eventually add unicode support for IPA symbols
    #I also define a for lopp over segments in the personal_output_formulas method
    # So make sure that the labels_list and the items in there are consistent

    self.input_symbols = list(set(self.labels_list) - set(['#','%']))
    self.copyset = [1,2,3]
    self.labels_are_input=  True


def personal_features(self):
    """Don't need because your input string is the string of labels"""

def personal_predicate_setup(self):
    """Give a list of your predicates as string"""
    self.predicates_list =  [ '[dat/loc]', '[nom/acc/voc]', '[gen/ nom/acc/voc pl]',
                            '[dat/loc pl/ins pl]',                           # syncretism
                            '[nom/acc/voc sg]' , '[dat/loc sg]', '[ins sg]',  #feature bundles
                            '[nom/acc/voc pl]', '[gen pl]', '[dat/loc pl]',
                            '[ins pl]',
                            '[pal]' ,                                       #phonology
                            'surfacing',                                    #I added this predicate to mean
                                                                            #it surfaces in the output
                            '[om/em_context]'                               #Had to make shared context for om/em
                            ]



def personal_Output_Formula(self, copy, label, domain_element):
    pred = self.get_value('input', 'function', 'pred', domain_element)
    pred_of_pred =  self.get_value('input', 'function', 'pred', pred)
    succ = self.get_value('input', 'function', 'succ', domain_element)

    u^1(x) = if dat/loc_sg(x) return T else u(x)
    u ^ 2(x) = if dat / loc_sg(x) return T else u^1(x)

    if copy is 1 and label == 'u':
        if self.get_value('input', 'predicate', '[dat/loc sg]', domain_element): return True
        else: return self.get_value('input', 'label', 'u', domain_element)
    #for stem-formant 't'
    if copy is 1 and label == 't':
        if self.get_value('input','label','+', domain_element):
            if self.get_value('input','label','e',pred):
                return self.get_value('input','predicate','surfacing',succ)
            else: return False
        else: return self.get_value('input','label','t',domain_element)
    #for the segment 'i' in ima
    if copy is 1 and label == 'i':
        if self.get_value('input', 'predicate', '[ins pl]', domain_element): return True
        else: return self.get_value('input', 'label', 'i', domain_element)
    #for the 'a' in suffixes aa and ima
    if copy is 1 and label == 'a':
        if self.get_value('input', 'predicate', '[gen/ nom/acc/voc pl]', domain_element): return True
        else: return  self.get_value('input', 'label', 'a', domain_element)
    if copy is 2 and label == 'a':
        if self.get_value('input', 'predicate', '[gen pl]', domain_element): return True
        else: return False
    if copy is 3 and label == 'a':
        if self.get_value('input', 'predicate', '[ins pl]', domain_element): return True
        else: return False
    #for the 'm' in suffixes 'om' and 'em' and 'ima'
    if copy is 2 and label == 'm':
        if self.get_value('input', 'label', '[ins]', domain_element): return True
        else: return False

    #om and em compete based on palatalization. Had to rewrite with om/em_context predicate
    if copy is 1 and label == 'o':
        if self.get_value('input', 'predicate', '[om/em_context]', domain_element): return True
        else: return self.get_value('input', 'label', 'o', domain_element)
    if copy is 1 and label == 'e':
        if self.get_value('input', 'predicate', '[om/em_context]', domain_element):
            if self.get_value('input','label','+',pred):
                return self.get_value('input','predicate','[pal]',pred_of_pred)
            else: return False
        else: return self.get_value('input', 'label', 'e', domain_element)

    #for every other segment
    if copy is 1 and label in [ 'b', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'n', 'p', 'r', 's', 'v', 'z']:
        return self.get_value('input','label',label,domain_element)


    #remove + in output
    #remove case markers in output
    #This is done by default by not giving them output functions

def personal_Predicate_Formula(self,predicate,domain_element):

    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)


    #Syncretism of feature-bundles
    if predicate == '[dat/loc]':
        if self.get_value('input', 'label', '[dat]', domain_element): return True
        else: return self.get_value('input', 'label', '[loc]', domain_element)
    if predicate == '[nom/acc/voc]':
        if self.get_value('input', 'label', '[nom]', domain_element): return True
        elif self.get_value('input', 'label', '[acc]', domain_element): return True
        else: return self.get_value('input', 'label', '[voc]', domain_element)
    if predicate == '[gen/ nom/acc/voc pl]':
        if self.get_value('input', 'label', '[gen]', domain_element): return True
        else: return self.get_value('input', 'predicate', '[nom/acc/voc pl]', domain_element)
    if predicate == '[dat/loc pl/ins pl]':
        if self.get_value('input', 'predicate', '[dat/loc pl]', domain_element): return True
        else: return self.get_value('input', 'predicate', '[ins pl]', domain_element)

    #Feature-bundles
    if predicate == '[nom/acc/voc sg]':
        if self.get_value('input','predicate','[nom/acc/voc]', domain_element):
            return self.get_value('input','label','[sg]', domain_element)
        else: return False
    if predicate == '[dat/loc sg]':
        if self.get_value('input','predicate','[dat/loc]', domain_element):
            return self.get_value('input','label','[sg]', domain_element)
        else: return False
    if predicate == '[ins sg]':
        if self.get_value('input','label','[ins]', domain_element):
            return self.get_value('input','label','[sg]', domain_element)
        else: return False
    if predicate == '[nom/acc/voc pl]':
        if self.get_value('input','predicate','[nom/acc/voc]', domain_element):
            return self.get_value('input','label','[pl]', domain_element)
        else: return False
    if predicate == '[gen pl]':
        if self.get_value('input','label','[gen]', domain_element):
            return self.get_value('input','label','[pl]', domain_element)
        else: return False
    if predicate == '[dat/loc pl]':
        if self.get_value('input','predicate','[dat/loc]', domain_element):
            return self.get_value('input','label','[pl]', domain_element)
        else: return False
    if predicate == '[ins pl]':
        if self.get_value('input', 'label', '[ins]', domain_element):
            return self.get_value('input', 'label', '[pl]', domain_element)
        else: return False

    #Phonology
    #Need to add labels for IPA palatals
    if predicate == '[pal]':
        if self.get_value('input', 'label', 'j', domain_element): return True
        else: return False

    #Extra
    #I added this feature to mean the domain element surfaces in the output by having any of the output labels
    #The BMRS format would need a long sequence of if-else clauses. I will cheat with a for loop
    #It's also counter-intuitive because predicates are defined over the input so the input element has the predicate
    #'surfacing' if it has an output correspondent x' in copy 1 such that x' has an output label
    if predicate == 'surfacing':
        for label in self.labels_list:
            if self.get_value(1,'label',label,domain_element):
                return True
        return False

    #Had to make shared context for om-em because they're allomorphs based on palatalization
    if predicate == "[om/em_context]":
        if self.get_value('input', 'predicate', '[nom/acc/voc sg]', domain_element): return True
        else: return  self.get_value('input', 'predicate', '[ins sg]', domain_element)



