#Automatically generated Python file from YAML:ex2-fully-explicit
def personal_setup(self):
	self.input_symbols = [ 'd', 'c', 'b', 'a' ]
	self.labels_list = [ 'd', 'c', 'b', 'a', '%', '#' ]
	self.copyset = [1, 2]
	self.labels_are_input = True
def personal_features(self):
	return
def personal_predicate_setup(self):
	self.predicates_list = [ 'foo', 'word-final', 'word-initial' ]
def personal_OutputLabel_Formula(self, label, node):
	copy,domain_element = node
	if copy is 1 and label == "a":
		if self.get_BooleanValue('label','a',(0,self.get_NodeDomain((0,domain_element)))):
			if self.get_BooleanValue('predicate','word-initial',(0,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element))))):
				return True
			else:
				return self.get_BooleanValue('label','b',(1,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element)))))
		else:
			return False
	if copy is 2 and label == "a":
		return False
	if copy is 1 and label == "b":
		if self.get_BooleanValue('label','a',(0,self.get_NodeDomain((0,domain_element)))):
			return self.get_BooleanValue('label','a',(1,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element)))))
		else:
			return False
	if copy is 2 and label == "b":
		if self.get_BooleanValue('label','a',(0,self.get_NodeDomain((0,domain_element)))):
			return self.get_BooleanValue('label','a',(1,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element)))))
		else:
			return False
	if copy is 1 and label == "c":
		if self.get_BooleanValue('predicate','word-final',(0,self.get_NodeDomain((0,domain_element)))):
			return self.get_BooleanValue('label','b',(1,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element)))))
		else:
			return False
	if copy is 2 and label == "c":
		return False
	if copy is 1 and label == "d":
		if self.get_BooleanValue('predicate','word-final',(0,self.get_NodeDomain((0,domain_element)))):
			return self.get_BooleanValue('label','a',(1,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element)))))
		else:
			return False
	if copy is 2 and label == "d":
		return False
	if copy is 1 and label == "%":
		return False
	if copy is 2 and label == "%":
		return False
	if copy is 1 and label == "#":
		return False
	if copy is 2 and label == "#":
		return False
	return False
def personal_Predicate_Formula(self,predicate,node):
	level,domain_element = node
	if level is 0 and predicate == 'foo':
		return True
	if level is 0 and predicate == 'word-final':
		return self.get_BooleanValue('label','%',(0,self.get_NodeDomain((0,domain_element))))
	if level is 0 and predicate == 'word-initial':
		return self.get_BooleanValue('label','#',(0,self.get_NodeDomain((0,domain_element))))
	return False
