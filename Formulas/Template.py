"""Here's a template
Replace TO DO with your own code
"""

def personal_setup(self):
    """Make sure that you include the symbols # and % in your list of labels"""
    self.labels_list = ['#', '%', TO DO ]
    """List the copies in your copy set, e.g., [1] or [1,2] or [1,2,3] or etc."""
    self.copyset = TO DO
    #Example:
    #self.copyset = [1]
    """Wil you write your input strings using the above labels? if yes, then assign the following boolean to true 
    Otherwise, assign it to false
    Generally, assign the boolean to true if you will use generic symbols like {a,b,c,...}, but set it to false if 
    you will use phonological faetures but represent your input strings with letters"""

    self.labels_are_input= TO DO
    #Example:
    #self.labels_are_input= False

def personal_features(self):
    """If you will repesent your input strings with symbols, but use features for your labels,
    then fill this table with your segment-to-feature decomposition. See the example of Intervocalic voicing for
     an example.
     Make sure you keep the word boundares
     Make sure to use frozenset over a list"""
    self.segment_to_labels = {
        '#': frozenset(['#']),
        '%': frozenset(['%']),
        TO DO
    #Example:
    #    'p': frozenset(['labial', 'consonant']),
     #   'L\'': frozenset(['L', 'stress']),

    }
    self.labels_to_symbols = {v: k for k, v in self.segment_to_labels.items()}

def personal_predicate_setup(self):
    """Give a list of your predicates as string"""
    self.predicates_list = TO DO
    #Example:
    # self.predicates_list = ['initial','final','syll','clash','lapse','only']



def personal_Output_Formula(self, copy, label, domain_element):
    """For every output function, decompose it into the following sequence of if-else clauses:
    if copy is X and label == Y:
        if Z:...

    Make sure to use return statements

    When referring to an input label, use the formula "self.input_to_labels[L].get(D)"
    where L is the label (in strings) and D is the domain element (integer)

    When referring to an input function, use the formula "self.input_to_functions[F].get(D)"
    where F is the function (in strings) and D is the domain element (integer)

    When referring to a predicate value over the input,  use the formula "self.get_predicate_value(P,D)
    where P is the predicate (in strings) and D is the domain element (integer)"

    When referring to the value of an output node,  use the formula "self.get_output_value(C,L,D)
    where C is the copy (integer), L is the label (in strings), and D is the domain element (integer)"

     """

    """Example below. Delete"""
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)

    if copy is 1 and label == 'stress':
        if self.get_predicate_value('only',domain_element): return True
        elif self.get_predicate_value('final',domain_element): return False
        elif self.input_to_labels['H'].get(domain_element): return True
        elif self.get_predicate_value('initial',domain_element):return False
        elif self.get_predicate_value('clash',domain_element): return False
        else: return self.get_predicate_value('lapse',domain_element)
    if copy == 1 and label == 'H':
        if self.get_output_value(1, 'stress', domain_element): return True
        else: return self.input_to_labels['H'].get(domain_element)
    if copy == 1 and label == 'L':
        if self.get_output_value(1, 'stress', domain_element): return False
        else: return self.input_to_labels['L'].get(domain_element)


def personal_Predicate_Formula(self,predicate,domain_element):
    """For every predicate formula, decompose it into the following sequence of if-else clauses:
    if predicate == Y:
        if Z:...

    Make sure to use return statements

    When referring to an input label, use the formula "self.input_to_labels[L].get(D)"
    where L is the label (in strings) and D is the domain element (integer)

    When referring to an input function, use the formula "self.input_to_functions[F].get(D)"
    where F is the function (in strings) and D is the domain element (integer)

    When referring to a predicate value over the input,  use the formula "self.get_predicate_value(P,D)
    where P is the predicate (in strings) and D is the domain element (integer)"

    When referring to the value of an output node,  use the formula "self.get_output_value(C,L,D)
    where C is the copy (integer), L is the label (in strings), and D is the domain element (integer)"

     """
    pred = self.input_to_functions['pred'].get(domain_element)
    succ = self.input_to_functions['succ'].get(domain_element)

    """Example below. Delete"""
    if predicate == 'final':
        if self.input_to_labels['%'].get(succ): return True
        else: return False
    if predicate == 'initial':
        if self.input_to_labels['%'].get(pred): return True
        else: return False
    if predicate == 'syll':
        if self.input_to_labels['L'].get(domain_element): return True
        else:
            return self.input_to_labels['H'].get(domain_element)
    if predicate == 'clash':
        if self.get_predicate_value('syll', domain_element):
            return self.get_output_value(1, 'stress', pred)
        else:
            return False
    if predicate == 'lapse':
        if self.get_output_value(1,'stress',pred): return False
        else:
            if self.get_predicate_value('syll',pred): return self.get_predicate_value('syll',domain_element)
            else: return False
    if predicate == 'only':
        if self.get_predicate_value('final',domain_element):
            return self.get_predicate_value('initial',domain_element)
        else:
            if self.get_predicate_value('final',succ):
                return self.get_predicate_value('initial',domain_element)
            else: return False