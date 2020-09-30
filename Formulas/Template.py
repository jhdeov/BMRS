"""Here's a template
Replace TO DO with your own code
"""

def personal_setup(self):
    """Make sure that you include the symbols # and % in your list of labels"""
    self.labels_list = ['#', '%',  "REPLACE ME" ]

    """If you wil represent your input strings with symbols that differ from your labels, e.g., phonological features 
    labels and phonological segments for your strings, then specify your list of segments"""
    self.input_symbols = ["REPLACE ME"]

    """List the copies in your copy set, e.g., [1] or [1,2] or [1,2,3] or etc."""
    self.copyset = "REPLACE ME"
    #Example:
    #self.copyset = [1]
    """Wil you write your input strings using the above labels? if yes, then assign the following boolean to true 
    Otherwise, assign it to false
    Generally, assign the boolean to true if you will use generic symbols like {a,b,c,...}, but set it to false if 
    you will use phonological faetures but represent your input strings with letters"""

    self.labels_are_input=  "REPLACE ME"
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
        "REPLACE ME": frozent([ "REPLACE ME"]),
    #Example:
    #    'p': frozenset(['labial', 'consonant']),
     #   'L\'': frozenset(['L', 'stress']),

    }
    self.labels_to_symbols = {v: k for k, v in self.segment_to_labels.items()}

def personal_predicate_setup(self):
    """Give a list of your predicates as string"""
    self.predicates_list =  "REPLACE ME"
    #Example:
    # self.predicates_list = ['initial','final','syll','clash','lapse','only']



def personal_Output_Formula(self, copy, label, domain_element):
    """For every output function, decompose it into the following sequence of if-else clauses:
    if copy is X and label == Y:
        if Z:...

    Make sure to use return statements

    When referring to an input label, use the formula "self.get_value('input','label',L,D)"
    where L is the label (in strings) and D is the domain element (integer)

    When referring to an input function, use the formula "self.get_value('input','function',F,D)"
    where F is the function (in strings) and D is the domain element (integer)

    When referring to a predicate value over the input,  use the formula "self.get_value('input','predicate',P,D)"
    where P is the predicate (in strings) and D is the domain element (integer)"

    When referring to the label of an output node,  use the formula "self.get_value(C,'label',L,D)"
    where C is the copy (integer), L is the label (in strings), and D is the domain element (integer)"

     """

    """Example below. Delete"""
    pred = self.get_value('input', 'function', 'pred', domain_element)
    succ = self.get_value('input', 'function', 'succ', domain_element)

    if copy is 1 and label == 'stress':
        if self.get_value('input', 'predicate', 'only', domain_element):
            return True
        elif self.get_value('input', 'predicate', 'final', domain_element):
            return False
        elif self.get_value('input', 'label', 'H', domain_element):
            return True
        elif self.get_value('input', 'predicate', 'initial', domain_element):
            return False
        elif self.get_value('input', 'predicate', 'clash', domain_element):
            return False
        else:
            return self.get_value('input', 'predicate', 'lapse', domain_element)
    if copy == 1 and label == 'H':
        if self.get_value(1, 'label', 'stress', domain_element):
            return True
        else:
            return self.get_value('input', 'label', 'H', domain_element)
    if copy == 1 and label == 'L':
        if self.get_value(1, 'label', 'stress', domain_element):
            return False
        else:
            return self.get_value('input', 'label', 'L', domain_element)

def personal_Predicate_Formula(self,predicate,domain_element):
    """For every predicate formula, decompose it into the following sequence of if-else clauses:
    if predicate == Y:
        if Z:...

    Make sure to use return statements

    When referring to an input label, use the formula "self.get_value('input','label',L,D)"
    where L is the label (in strings) and D is the domain element (integer)

    When referring to an input function, use the formula "self.get_value('input','function',F,D)"
    where F is the function (in strings) and D is the domain element (integer)

    When referring to a predicate value over the input,  use the formula "self.get_value('input','predicate',P,D)"
    where P is the predicate (in strings) and D is the domain element (integer)"

    When referring to the label of an output node,  use the formula "self.get_value(C,'label',L,D)"
    where C is the copy (integer), L is the label (in strings), and D is the domain element (integer)"

     """


    pred = self.get_value('input','function','pred',domain_element)
    succ = self.get_value('input','function','succ',domain_element)

    if predicate == 'final':
        if self.get_value('input','label','%',succ): return True
        else: return False
    if predicate == 'initial':
        if self.get_value('input','label','%',pred): return True
        else: return False
    if predicate == 'syll':
        if self.get_value('input','label','L',domain_element): return True
        else:
            return self.get_value('input','label','H',domain_element)
    if predicate == 'clash':
        if self.get_value('input','predicate','syll', domain_element):
            return self.get_value(1,'label', 'stress', pred)
        else:
            return False
    if predicate == 'lapse':
        if self.get_value(1,'label','stress',pred): return False
        else:
            if self.get_value('input','predicate','syll',pred): return self.get_value('input','predicate','syll',domain_element)
            else: return False
    if predicate == 'only':
        if self.get_value('input','predicate','final',domain_element):
            return self.get_value('input','predicate','initial',domain_element)
        else:
            if self.get_value('input','predicate','final',succ):
                return self.get_value('input','predicate','initial',domain_element)
            else: return False