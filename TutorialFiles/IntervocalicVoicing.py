#Manually generated to do intervocalic voicing with features
def personal_setup(self):
	self.input_symbols = [ 'p',  'b','t','d','k','g','a','i','u' ]
	self.labels_list = ['voiced', 'labial', 'coronal', 'dorsal', 'low', 'high', 'front', 'back', 'cons', 'vowel',
						'#', '%']
	self.copyset = [1]
	self.labels_are_input = False



def personal_features(self):
    self.symbol_to_labels = {
        'p': frozenset(['cons', 'labial']),
        't': frozenset(['cons', 'coronal']),
        'k': frozenset(['cons', 'dorsal']),
        'b': frozenset(['cons', 'labial', 'voiced']),
        'd': frozenset(['cons', 'coronal', 'voiced']),
        'g': frozenset(['cons', 'dorsal', 'voiced']),
        'a': frozenset(['vowel', 'low', 'back', 'voiced']),
        'i': frozenset(['vowel', 'high', 'front', 'voiced']),
        'u': frozenset(['vowel', 'high', 'back', 'voiced']),
        '#': frozenset(['#']),
        '%': frozenset(['%'])
    }
    self.labels_to_symbols = {v: k for k, v in self.symbol_to_labels.items()}
def personal_predicate_setup(self):
	self.predicates_list = [ 'intervocalic' ]
	return
def personal_OutputLabel_Formula(self, label, node):
	copy,domain_element = node
	if copy == 1 and label == 'voiced':
		if self.get_BooleanValue('label', 'voiced', (0,domain_element)):
			return True
		else:
			if self.get_BooleanValue('label', 'cons', (0,domain_element)):
				if self.get_BooleanValue('predicate', 'intervocalic', (0,domain_element)):
					return True
				else:
					return False
			else:
				return False

	# Shortcut for the rest.
	if copy == 1 and label in self.labels_list and not (label == 'voiced' or label == '%' or label == '#'):
		return self.get_BooleanValue('label', label, (0,domain_element))

	return False
def personal_Predicate_Formula(self,predicate,node):
	level,domain_element = node
	if level is 0 and predicate == 'intervocalic':
		if self.get_BooleanValue('label','vowel',(0,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element))))):
			if self.get_BooleanValue('label','vowel',(0,self.get_NodeDomain(self.get_NodeValue('function','succ',(0,domain_element))))):
				return True
			else:
				return False
		else:
			return False
	return False
