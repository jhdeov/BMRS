#Automatically generated Python file from YAML:ex6-between-A-voicing
def personal_setup(self):
	self.input_symbols = [ 'p', 'a', 'b' ]
	self.labels_list = [ 'p', 'a', 'b', '%', '#' ]
	self.copyset = [1]
	self.labels_are_input = True
def personal_features(self):
	return
def personal_predicate_setup(self):
	self.predicates_list = [ 'betweenA' ]
	return
def personal_OutputLabel_Formula(self, label, node):
	copy,domain_element = node
	if copy is 1 and label == "a":
		if self.get_BooleanValue('label','a',(0,self.get_NodeDomain((0,domain_element)))):
			return True
		else:
			return False
	if copy is 1 and label == "p":
		if self.get_BooleanValue('label','p',(0,self.get_NodeDomain((0,domain_element)))):
			if self.get_BooleanValue('predicate','betweenA',(0,self.get_NodeDomain((0,domain_element)))):
				return False
			else:
				return True
		else:
			return False
	if copy is 1 and label == "b":
		if self.get_BooleanValue('label','b',(0,self.get_NodeDomain((0,domain_element)))):
			return True
		else:
			if self.get_BooleanValue('label','p',(0,self.get_NodeDomain((0,domain_element)))):
				if self.get_BooleanValue('predicate','betweenA',(0,self.get_NodeDomain((0,domain_element)))):
					return True
				else:
					return False
			else:
				return False
	return False
def personal_Predicate_Formula(self,predicate,node):
	level,domain_element = node
	if level is 0 and predicate == 'betweenA':
		if self.get_BooleanValue('label','a',(0,self.get_NodeDomain(self.get_NodeValue('function','pred',(0,domain_element))))):
			if self.get_BooleanValue('label','a',(0,self.get_NodeDomain(self.get_NodeValue('function','succ',(0,domain_element))))):
				return True
			else:
				return False
		else:
			return False
	return False
