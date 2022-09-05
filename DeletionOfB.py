#Automatically generated Python file from YAML:ex3-deletion-b
def personal_setup(self):
	self.input_symbols = [ 'b', 'a', 'd', 'e' ]
	self.labels_list = [ 'b', 'a', 'd', 'e', '%', '#' ]
	self.copyset = [1]
	self.labels_are_input = True
def personal_features(self):
	return
def personal_predicate_setup(self):
	return
def personal_OutputLabel_Formula(self, label, node):
	copy,domain_element = node
	if copy is 1 and label == "a":
		if self.get_BooleanValue('label','a',(0,self.get_NodeDomain((0,domain_element)))):
			return True
		else:
			return False
	if copy is 1 and label == "e":
		if self.get_BooleanValue('label','e',(0,self.get_NodeDomain((0,domain_element)))):
			return True
		else:
			return False
	if copy is 1 and label == "d":
		if self.get_BooleanValue('label','d',(0,self.get_NodeDomain((0,domain_element)))):
			return True
		else:
			return False
	return False
def personal_Predicate_Formula(self,predicate,node):
	level,domain_element = node
	return False
