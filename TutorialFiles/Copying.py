#Manually created: convert X to XX
def personal_setup(self):
	self.input_symbols = [ 'b',  'a','c'  ]
	self.labels_list = [ 'b',  'a','c' ,'%', '#' ]
	self.copyset = [1,2]
	self.labels_are_input = True
	self.OrderingStatus = "concatenative" 
def personal_features(self):
	return
def personal_predicate_setup(self):
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
	return

def personal_Predicate_Formula(self,predicate,node):
	return