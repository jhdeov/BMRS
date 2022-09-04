#Automatically generated Python file from YAML:ex2-fully-explicit
def personal_setup(self):
	self.input_symbols = [ 'b',  'a','c'  ]
	self.labels_list = [ 'b',  'a','c' ,'%', '#' ]
	self.copyset = [1,2]
	self.labels_are_input = True
	self.isOrderPreserving = False
def personal_features(self):
	return
def personal_predicate_setup(self):
	self.predicates_list = [ 'word-second', 'word-final', 'word-initial' ]
def personal_OutputLabel_Formula(self, label,node):
	copy,domain_element = node
	if (copy is 1 or copy is 2) and label == "a":
		# if self.get_BooleanValue('predicate','word-second',(0,domain_element)):
		# 	return False
		# if self.get_BooleanValue('predicate', 'word-final',(0,  domain_element)):
		# 	return False
		return self.get_BooleanValue('label','a',(0,domain_element))
	if (copy is 1 or copy is 2) and label == "b":
		return self.get_BooleanValue( 'label', 'b', (0,domain_element))
	# For all other copies and labels, the default is to return False so add the below
	# Makes it clearer
	return False

	# Change input to 0
def personal_OutputFunction_Formula(self,  function, node):
	copy,domain_element = node
	if copy is 1 and function == "succ":
		if self.get_BooleanValue('predicate','word-final',(0,domain_element)):
			return (2,domain_element)
		else:
			return (1,self.get_NodeDomain(self.get_NodeValue('function','succ',(0,domain_element))))
	if copy is 2 and function == "succ":
		return (2,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element))))
	if copy is 1 and function == "pred":
		return (1, self.get_NodeDomain(self.get_NodeValue('function', 'pred', (0, domain_element))))
	if copy is 2 and function == "pred":
		if self.get_BooleanValue('predicate', 'word-final', (0, domain_element)):
			return (1, domain_element)
		else:
			return (2, self.get_NodeDomain(self.get_NodeValue('function', 'succ', (0, domain_element))))


def personal_Predicate_Formula(self,predicate,node):
	level,domain_element = node

	if level is 0 and predicate == 'word-second':
		return self.get_BooleanValue('label','#',self.get_NodeValue('function','pred',self.get_NodeValue('function','pred',(0,domain_element))))
	if level is 0 and  predicate == 'word-final':
		return self.get_BooleanValue('label','%',self.get_NodeValue('function','succ',(0,domain_element)))
	if level is 0 and  predicate == 'word-initial':
		return self.get_BooleanValue('label','#',self.get_NodeValue('function','pred',(0,domain_element)))
