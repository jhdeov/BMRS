#Automatically generated Python file from YAML:ex8-repair-consonant-cluster
def personal_setup(self):
	self.input_symbols = [ 'a', 'p', 'ə' ]
	self.labels_list = [ 'a', 'p', 'ə', '%', '#' ]
	self.copyset = [1, 2]
	self.labels_are_input = True
def personal_features(self):
	return
def personal_predicate_setup(self):
	self.predicates_list = [ 'firstInCluster' ]
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
			return True
		else:
			return False
	if copy is 2 and label == "ə":
		if self.get_BooleanValue('predicate','firstInCluster',(0,self.get_NodeDomain((0,domain_element)))):
			return True
		else:
			return False
	return False
def personal_Predicate_Formula(self,predicate,node):
	level,domain_element = node
	if level is 0 and predicate == 'firstInCluster':
		if self.get_BooleanValue('label','p',(0,self.get_NodeDomain((0,domain_element)))):
			if self.get_BooleanValue('label','p',(0,self.get_NodeDomain(self.get_NodeValue('function','succ',(0,domain_element))))):
				return True
			else:
				return False
		else:
			return False
	return False
