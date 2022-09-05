"""Here's a template
TODO: any calls to functions must be fixed to add [1] to retrieve domain elements
"""

def personal_setup(self):
    """List what characters you accept as part of your input string
     Do not include the word boundaries '#' amd '%'.
     Individual features inside a feature bundle are fine.
     See the 'SerbianInflection.py' file for an example."""
    self.input_symbols = ['a','b','nom', "REPLACE ME"]

    """List what input labels you use. Make sure that you include the symbols # and % in your list of labels
    It's fine if your list of labels is the same as your input symbols, as long as '#' and '%' are included"""
    self.labels_list = ['#', '%',  "REPLACE ME" ]

    """List the copies in your copy set, e.g., [1] or [1,2] or [1,2,3] or etc."""
    self.copyset = "REPLACE ME"
    #Example:
    #self.copyset = [1]
    """Will you write your input strings using the above labels? if yes, then assign the following boolean to true 
    Otherwise, assign it to false
    Generally, assign the boolean to true if you will use generic symbols like {a,b,c,...}, but set it to false if 
    you will use phonological features but represent your input strings with letters"""

    self.labels_are_input=  "REPLACE ME"
    #Example:
    #self.labels_are_input= False

    """
    If you will write a rational function,  then set this variable to 'order-preserving' or delete it.'
    If you will write a non-rational concatenative function, then set this varaible to 'concatenative'. 
        See the 'Copying.py' file for an example.
    If you will write a non-rational non-order-preserving function, then set this varaible to 'other'.
        See the 'Mirroring.py' file for an exmaple."""
    self.OrderingStatus = "REPLACE ME"  #
    #Example:
    #self.copyset = 'order-preserving'

def personal_features(self):
    """If you will represent your input strings with symbols, but use features for your labels,
    then fill this table with your segment-to-feature decomposition.
    See the 'IntervocalicVoicing.py' file as an example.
     Make sure there's a 1-to-1 match between bundles of input labels and between input symbols
     Make sure you keep the word boundares
     Make sure to use frozenset over a list"""
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
    self.predicates_list =  "REPLACE ME"
    #Example:
    # self.predicates_list = ['initial','final','syll','clash','lapse','only']

    return

def personal_OutputLabel_Formula(self, label,node):
    copy,domain_element = node

    """For every output formula, decompose it into the following sequence of if-else clauses:
    if copy is X and label == Y:
        if Z:...

    Make sure to use return statements

    When referring to the Boolean value of a label over the input, use the formula "self.get_BooleanValue('label',L,(0,D))"
    where 0 is the input level, L is the label (in strings) and D is the domain element (integer)

    When referring to a Boolean value of a predicate over the input,  use the formula "self.get_BooleanValue('predicate',P,(0,D))"
    where 0 is the input level, P is the predicate (in strings) and D is the domain element (integer)"

    When referring to the node value of a function like successor over the input, use the formula "self.get_NodeValue('function',F,(0,D))"
    where 0 is the input level, F is the function (in strings) and D is the domain element (integer)
    
    If you need to access the domain element of a node, use the formula "self.get_NodeDomain(N)"
    where N is a node.
    This formula is needed if you try to examine the labels of a node that was retrieved from a function.
    For example, to check if the predecessor of 'x' over the input has the label 'a', then use the following:
        self.get_BooleanValue('label','a',(0,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,x)))))

    When referring to any of the above values for output node, replace the symbol 0 with C
    where C is the copy (integer), L is the label (in strings), and D is the domain element (integer)"

     """

    """Example below"""

    if copy is 1 and label == 'stress':
        if self.get_BooleanValue('predicate', 'only', (0,domain_element)):
            return True
        elif self.get_BooleanValue('predicate', 'final', (0,domain_element)):
            return False
        elif self.get_BooleanValue('label', 'H', (0,domain_element)):
            return True
        elif self.get_BooleanValue('predicate', 'initial', (0,domain_element)):
            return False
        elif self.get_BooleanValue('predicate', 'clash', (0,domain_element)):
            return False
        else:
            return self.get_BooleanValue('predicate', 'lapse', (0,domain_element))
    if copy == 1 and label == 'H':
        if self.get_BooleanValue('label', 'stress', (1,domain_element)):
            return True
        else:
            return self.get_BooleanValue('label', 'H', (0, domain_element))
    if copy == 1 and label == 'L':
        if self.get_BooleanValue('label', 'stress', (1,domain_element)):
            return False
        else:
            return self.get_BooleanValue('label', 'L', (0,domain_element))
    
    """This must be the last statement in this method"""
    return False
def personal_Predicate_Formula(self,predicate,node):
    level,domain_element = node
    """For every predicate formula, decompose it into the following sequence of if-else clauses:
    if level is X and predicate == Y:
        if Z:...

    Make sure to use return statements

    See the method 'personal_OutputLabel_Formula' for explanation on how get label values and nodes.

     """

    if level is 0 and predicate == 'final':
        if self.get_BooleanValue('label','%',(0,self.get_NodeDomain(self.get_NodeValue('function','succ',(0,domain_element))))): return True
        else: return False
    if level is 0 and predicate == 'initial':
        if self.get_BooleanValue('label','#',(0,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element))))): return True
        else: return False
    if level is 0 and predicate == 'syll':
        if self.get_BooleanValue('label','L',(0,domain_element)): return True
        else:
            return self.get_BooleanValue('label','H',(0,domain_element))
    if level is 0 and predicate == 'clash':
        if self.get_BooleanValue('predicate','syll', (0,domain_element)):
            return self.get_BooleanValue('label', 'stress', (1,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element)))))
        else:
            return False
    if level is 0 and predicate == 'lapse':
        if self.get_BooleanValue('label','stress',(1,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element))))): return False
        else:
            if self.get_BooleanValue('predicate','syll',(0,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element))))): return self.get_BooleanValue('input','predicate','syll',domain_element)
            else: return False
    if level is 0 and predicate == 'only':
        if self.get_BooleanValue('predicate','final',(0,domain_element)):
            return self.get_BooleanValue('predicate','initial',(0,domain_element))
        else:
            if self.get_BooleanValue('predicate','final',(0,self.get_NodeDomain(self.get_NodeValue('function','succ',(0,domain_element))))):
                return self.get_BooleanValue('predicate','initial',(0,domain_element))
            else: return False
    
    """This must be the last statement in this method"""
    return False