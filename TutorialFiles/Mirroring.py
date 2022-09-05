#Manually created: convert X to XXʳ
def personal_setup(self):
	self.input_symbols = [ 'b',  'a','c'  ]
	self.labels_list = [ 'b',  'a','c' ,'%', '#' ]
	self.copyset = [1,2]
	self.labels_are_input = True
	self.OrderingStatus = "other" #
def personal_features(self):
	return
def personal_predicate_setup(self):
	self.predicates_list = [  'word-final' ]
	return
def personal_OutputLabel_Formula(self, label,node):
	copy,domain_element = node
	if copy is 1 and label == "a":
		return self.get_BooleanValue('label', 'a', (0, domain_element))
	if copy is 1 and label == "b":
		return self.get_BooleanValue('label', 'b', (0, domain_element))
	if copy is 1 and label == "c":
		return self.get_BooleanValue('label', 'c', (0, domain_element))
	if copy is 2 and label == "a":
		return self.get_BooleanValue('label','a',(0,domain_element))
	if copy is 2 and label == "b":
		return self.get_BooleanValue('label','b',(0,domain_element))
	if copy is 2 and label == "c":
		return self.get_BooleanValue('label','c',(0,domain_element))
	return False

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
	return (None,None)

def personal_Predicate_Formula(self,predicate,node):
	level,domain_element = node

	if level is 0 and  predicate == 'word-final':
		return self.get_BooleanValue('label','%',self.get_NodeValue('function','succ',(0,domain_element)))
	return False