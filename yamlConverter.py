import codecs
import sys

class YamlComponent:
    def __init__(self,name,original_content=[]):
        self.name = name
        self.original_content = original_content
        self.info_for_python = []
    def __str__(self):
        return f"name: {self.name}\n" \
               f"original_content: {self.original_content}\n" \
               f"info_for_python: {self.info_for_python}"

    def fillInputOutputAlphabet(self,yamlContent):
        assert self.name == "alphabet"
        assert yamlContent[0] == "def-input-alphabet" or yamlContent[0] == "def-output-alphabet"
        print(f"Filling up input/output alphabet with content:\n{yamlContent}")
        assert len(yamlContent) == 2
        assert type(yamlContent[1]) == list
        assert yamlContent[1][0] == 'list'
        self.original_content=yamlContent
        alphabet_items = set([])
        for alphabet_item in yamlContent[1][1:]:
            assert alphabet_item[0] == '"'
            assert alphabet_item[-1] == '"'
            alphabet_items.add(alphabet_item[1:-1])
        print(f'Creating following list for input alphabet\n{alphabet_items}')
        # The python code treats #,% as special characters that aren't written in the input string
        alphabet_items.remove('#')
        alphabet_items.remove('%')
        if len(self.info_for_python) is 0:
            self.info_for_python= alphabet_items
        else:
            self.info_for_python= self.info_for_python.union(alphabet_items)
    def fillCopySetSize(self,yamlContent):
        assert self.name == "copyset"
        assert yamlContent[0] == "def-copy-set-size"
        print(f"Filling up copyset size with content:\n{yamlContent}")
        assert len(yamlContent) == 2
        assert type(yamlContent[1]) == str
        self.original_content=yamlContent
        copysetsize_int = int(yamlContent[1])
        self.info_for_python= copysetsize_int

class yamlConversion:
    def __init__(self,originalYaml,pythonFileName):

        print("Useful debugging info for conversion is printed into the conversion.message.log")
        # The printing code was taken from https://stackoverflow.com/a/2513511
        old_stdout = sys.stdout
        log_file = open(originalYaml + ".conversion.message.log", "w")
        sys.stdout = log_file

        self.originalYaml = originalYaml
        self.pythonFileName = pythonFileName
          # convert YAML to list
        self.codeToProcess = self.yamlToList(self.originalYaml)

        #set up obligatory yaml components for the python version
        self.inputoutput_alphabet_yaml = YamlComponent(name="alphabet")
        self.copysetsize_yaml = YamlComponent(name="copyset")
        self.predicateList_yaml = []
        self.outputFunctList_yaml = []

        # assert that the yaml-list has the right structure
        assert len(self.codeToProcess) == 1
        assert self.codeToProcess[0][0] == 'def-transduction'

        self.transduction_name = self.codeToProcess[0][1]
        print(f'\nTransuction is for {self.transduction_name}')

        # go through each line in the yaml file and extract the useful information for conversion
        print("\nWill now read through each line of the Yaml file and extract Yaml components")
        for yamlComponent in self.codeToProcess[0][2:]:
            print(f'\tReading component:\n{yamlComponent}')
            yamlComponentName = yamlComponent[0]
            if yamlComponentName ==  'def-input-alphabet':
                self.inputoutput_alphabet_yaml.fillInputOutputAlphabet(yamlComponent)
                print(f'\t->Updated input/output alphabet:\n{self.inputoutput_alphabet_yaml}')
            elif yamlComponentName == 'def-output-alphabet':
                self.inputoutput_alphabet_yaml.fillInputOutputAlphabet(yamlComponent)
                print(f'\t->Updated input/output alphabet:\n{self.inputoutput_alphabet_yaml}')
            elif yamlComponentName == 'def-copy-set-size':
                self.copysetsize_yaml.fillCopySetSize(yamlComponent)
                print(f'\t->Updated copyset size:\n{self.copysetsize_yaml}')
            elif yamlComponentName == 'def-predicate':
                self.insertPredicateYamlToList(yamlComponent)
                print(f'->Updated predicate list:\n{self.predicateList_yaml}')
            elif yamlComponentName == 'def-output':
                self.insertOutputFunctYamlToList(yamlComponent)
                print(f'->Updated output label function list:\n{self.outputFunctList_yaml}')
            else:
                print(f'This Yaml component could not be processed:{yamlComponent}')
                exit()

        print("\nFinished reading the Yaml file; will now convert to Python")
        print('\n1) Creating the input alphabet (input symbols)')
        self.processInputAlphabet()
        print('\n2) Creating feature set')
        self.processLabelFeatureSet()
        print('\n3) Creating the copy set')
        self.processCopySet()
        print('\n4) Creating the predicate code')
        self.processPredicateList()
        print('\n5) Creating the output label function code')
        self.processOutputLabelFormulaList()

        print("\nCreating the python file")
        self.createPythonFile()

        sys.stdout = old_stdout
        log_file.close()

    # push and parse_parentheses were taken from https://stackoverflow.com/a/50702934
    def push(self,obj, l, depth):
        while depth:
            l = l[-1]
            depth -= 1
        #I adapted this so that characters form strings, not separate list items
        #print(f"gonna append {obj} to {l}")
        if len(l) is 0:
            l.append(obj)
        elif len(obj) is 0:
            if l[-1][-1] is " ": # this to prevent cases like ["foo ", ['x]]
                l[-1] = l[-1].strip()
            l.append(obj)
        elif type(l[-1]) is list:
            if obj is not ' ': # this is to prevent cases like [['x'], " "]
                 l.append(obj)
        elif l[-1][-1] is " ":
            l[-1] = l[-1].strip()
            l.append(obj)
        else:
            l[-1] = l[-1] + obj
        #print(f"appended: {l}")

    def parse_parentheses(self,s):
        groups = []
        depth = 0

        try:
            for char in s:
                if char == '(':
                    self.push([], groups, depth)
                    depth += 1
                elif char == ')':
                    depth -= 1
                else:
                    self.push(char, groups, depth)
        except IndexError:
            raise ValueError('Parentheses mismatch')

        if depth > 0:
            raise ValueError('Parentheses mismatch')
        else:
            return groups

    def yamlToList(self,originalYaml):
        # Given a YAML file, convert it into a list
        print("Creating a cleaned up YAML file")
        outFileCleaned = originalYaml[:-4] + "_cleaned.txt"
        codeToProcess = ""
        with codecs.open(originalYaml, 'r', 'utf-8') as iFile:
            with codecs.open(outFileCleaned, 'w', 'utf-8') as o:
                lines = iFile.read().splitlines()
                lines[0] = lines[0].replace('\ufeff', "")
                for line in lines:
                    print(f"\tReading in line:{line}")
                    # Remove comments, taken from https://stackoverflow.com/a/904758
                    head, sep, tail = line.partition('--')
                    headStripped = head.strip()
                    headStripped = headStripped.replace('  ',' ') # to remove any extra spaces that'll confuse the parser
                    if len(headStripped)>0:
                        o.writelines(head+  "\n")
                        codeToProcess = codeToProcess + headStripped + ' '
        print(f'Reading the following code:\n{(codeToProcess)}')
        codeToProcess = self.parse_parentheses(codeToProcess)
        print("->YAML file is parsed to the following list")
        print(codeToProcess)
        print("->A more readable version of the list:")
        for i in range(len(codeToProcess[0])):
            print(codeToProcess[0][i])
        return codeToProcess
    def insertPredicateYamlToList(self,yamlContent):
        assert yamlContent[0] == "def-predicate"
        print(f"Adding a predicate-yaml to the predicate list"
              f"\n{yamlContent}")
        assert len(yamlContent) == 4
        self.original_content=yamlContent
        predicate_name = yamlContent[1]
        predicate_node = yamlContent[2]
        predicate_logic = yamlContent[3]
        self.predicateList_yaml.append({'name':predicate_name,'node':predicate_node,'logic':predicate_logic})
    def insertOutputFunctYamlToList(self,yamlContent):
        assert yamlContent[0] == "def-output"
        print(f"Adding a output-yaml to the output-function list"
              f"\n{yamlContent}")
        assert len(yamlContent) == 5
        self.original_content=yamlContent
        output_name = yamlContent[1]
        output_copy = yamlContent[2]
        output_node= yamlContent[3]
        output_logic = yamlContent[4]
        self.outputFunctList_yaml.append({'name':output_name,'copy':output_copy,'node':output_node,'logic':output_logic})
    def processLabelFeatureSet(self):
        #TODO: rewrite this after eric figures out features
        self.inputLabelFeaturesPython =  """\tself.labels_list = [ """
        for label in self.inputoutput_alphabetList[:-1]:
            print(f'Working on:{label}')
            self.inputLabelFeaturesPython = self.inputLabelFeaturesPython + f"'{label}', "
            print(f'Added:\n{self.inputLabelFeaturesPython}')
        self.inputLabelFeaturesPython = self.inputLabelFeaturesPython + f"'{self.inputoutput_alphabetList[-1]}' ]"
        print(f'->Finished creating python code for label/features:\n{self.inputLabelFeaturesPython}')
    def processInputAlphabet(self):
        self.inputoutput_alphabetPython = """\tself.input_symbols = [ """
        self.inputoutput_alphabetList = list(self.inputoutput_alphabet_yaml.info_for_python)
        for symbol in (self.inputoutput_alphabetList)[:-1]:
            print(f'Working on:{symbol}')
            self.inputoutput_alphabetPython = self.inputoutput_alphabetPython + f"'{symbol}', "
            print(f'Added:\n{self.inputoutput_alphabetPython}')
        self.inputoutput_alphabetPython = self.inputoutput_alphabetPython + f"'{self.inputoutput_alphabetList[-1]}' ]"
        print(f'->Finished creating python code for alphabet:\n{self.inputoutput_alphabetPython}')
        self.inputoutput_alphabetList = self.inputoutput_alphabetList + ['%','#']
        print(f'Had to include #,% in our list of symbols, but not in the python code:\n{self.inputoutput_alphabetList}')
    def processCopySet(self):#
        self.copySetMaxValue = self.copysetsize_yaml.info_for_python
        self.copySetPython = f'\tself.copyset = {list(range(self.copySetMaxValue+1))[1:]}'
        print(f'->Finished creating python code for copyset:\n{self.copySetPython}')


    def processOutputLabelFormulaList(self):
        self.outputLabelFormulaPythonList = []
        for outputLabelFunction_listifid_yaml in self.outputFunctList_yaml:
            print(f'Working on output label function code from yaml:\n{outputLabelFunction_listifid_yaml}')
            outputLabelFormula_label = outputLabelFunction_listifid_yaml['name']
            outputLabelFormula_copy = outputLabelFunction_listifid_yaml['copy']
            outputLabelFormula_node = outputLabelFunction_listifid_yaml['node']
            assert outputLabelFormula_node == ['x']
            outputLabelFormula_logicYaml = outputLabelFunction_listifid_yaml['logic']
            outputLabelFormula_python_ListItem =f'\tif copy is {outputLabelFormula_copy} and label == {outputLabelFormula_label}:'
            logicBody = self.processLogicBody(outputLabelFormula_logicYaml,"\t\t")
            outputLabelFormula_python_ListItem = outputLabelFormula_python_ListItem + f"\n{logicBody}"
            print(f'->Created:\n{outputLabelFormula_python_ListItem}')
            outputLabelFormula_python_ListItem = self.addReturnsToLogicBody(outputLabelFormula_python_ListItem)
            print(f'->Cleaned up with returns:\n{outputLabelFormula_python_ListItem}')

            self.outputLabelFormulaPythonList.append(outputLabelFormula_python_ListItem)


    def processPredicateList(self):
        print('Creating python code for predicate names')
        self.predicateListNames = []
        self.predicateListNamePython = ""
        self.predicateLogicPython = []
        for predicateYaml in self.predicateList_yaml:
            print(f'Reading predicate-yaml: {predicateYaml}')
            self.predicateListNames.append(predicateYaml['name'])
        if len(self.predicateListNames) is 0:
            print("There are no predicates to creates")
        else:
            self.predicateListNamePython = f"\tself.predicates_list = [ "
            for predicateName in self.predicateListNames[:-1]:
                print(f'Working on:{predicateName}')
                self.predicateListNamePython = self.predicateListNamePython + f"'{predicateName}', "
                print(f'Added:\n{self.predicateListNamePython}')
            self.predicateListNamePython = self.predicateListNamePython + f"'{self.predicateListNames[-1]}' ]"
            print(f'->Finished creating python code for predicate names:\n{self.predicateListNamePython}')

            print(f'->Creating the following list of predicates: {self.predicateListNames}')

            for predicateYaml in self.predicateList_yaml:
                predicateText = f"\tif level is 0 and predicate == '{predicateYaml['name']}':"
                assert predicateYaml['node'] == ['x']
                logicBody=self.processLogicBody(predicateYaml['logic'],"\t\t")
                predicateText = predicateText + f"\n{logicBody}"
                print(f'Created:\n{predicateText}')
                predicateText=self.addReturnsToLogicBody(predicateText)
                print(f'Cleaned up with returns:\n{predicateText}')
                self.predicateLogicPython.append(predicateText)

    def processLogicBody(self,text,tabs):
        print(f'Logical text to process:{text}')
        if text == "'true":
            return f'{tabs}True'
        elif text == "'false":
                return f'{tabs}False'
        elif len(text) is 2:
            # Checks if the yaml codeblock is like (#_0 x) or (predicate x)')
            labelOrPred,copy,node= None, None, None
            firstElement =  text[0]
            secondElement = text[1]
            if self.isLabelUnderCopy(firstElement):
                labelOrPred, copy = self.convertLabelUnderCopy(firstElement)
                islabelOrPred = self.strLabelOrPred(labelOrPred)
                copy = self.strCopyIndex(copy)
            elif firstElement in self.predicateListNames:
                islabelOrPred, labelOrPred, copy = "predicate",firstElement,"0"
            node = self.processNodeFinding(secondElement)
            # Right now, the nodeFinding method is used to retrieve a node (copy,domain_element)
            # But if an output-label function is calling this, then we just need the domain element which we have to extract
            # Once we incorpoate output-function formula, then this will need to be revised
            # TODO: what we need is to incorporate indexing better in the YAML
            logicbody = f"{tabs}self.get_BooleanValue('{islabelOrPred}','{labelOrPred}',({copy},self.get_NodeDomain({node})))"
            print(f'->Processed this body and returned:{logicbody}')
            return logicbody
        elif len(text) is 4:
            # Checks if the yaml codebloc is like (if CONDITION RESULT OTHERWISE
            firstIf,secondCondYaml,thirdRes,fourthElse = text
            assert firstIf == 'if'
            secondCondLogic = self.processLogicBody(secondCondYaml,'')
            logicbody = f'{tabs}if {secondCondLogic}:\n'
            thirdResultLogic = self.processLogicBody(thirdRes,f'{tabs}\t')
            logicbody = f"{logicbody}{thirdResultLogic}"
            fourthElseLogic = self.processLogicBody(fourthElse,f"{tabs}\t")
            logicbody = f"{logicbody}\n{tabs}else:\n{fourthElseLogic}"
            return logicbody

            # if copy is 1 and label == 'stress':
            #     if self.get_value('input', 'predicate', 'only', domain_element):
            #         return True

        else:
            print(f'Error, unknown logical template')
            exit()
    def processNodeFinding(self,text):
        print(f"Finding node with info:{text}")
        if text == 'x':
            return '(0,domain_element)'
        elif type(text) is list and len(text) is 2:
            firstElement,secondElement = text[0],text[1]
            if firstElement ==  'pred':
                return f"self.get_NodeValue('function','pred',{self.processNodeFinding(secondElement)})"
            elif firstElement ==  'succ':
                return f"self.get_NodeValue('function','succ',{self.processNodeFinding(secondElement)})"
            else:
                print(f"Error, can't find a node with info:{text}")
                exit()
        else:
            print(f"Error, can't find a node with info:{text}")
            exit()
    def strCopyIndex(self,text):
        zeroTillCopyMax = (list(range(self.copySetMaxValue+1)))
        assert text in zeroTillCopyMax
        return text
    def strLabelOrPred(self,text):
            if text in self.predicateListNames:
                return 'predicate'
            elif text in self.inputLabelFeaturesPython:
                return 'label'
            else:
                print(f'Error, this unit {text} is not in labels or predicates')
                exit()
    def isLabelUnderCopy(self,text):
        if '_' in text:
            text = text.split('_')
            if len(text) is 2:
                return True
        return False
    def convertLabelUnderCopy(self,text):
        assert self.isLabelUnderCopy(text)
        text = text.split('_')
        assert len(text) is 2
        label = text[0]
        copy = int(text[1])
        return(label,copy)

    def addReturnsToLogicBody(self,text):
        # Add 'return' statements to any logic-body line that doesn't start with 'if' or 'else'
        textWithReturns = text.split('\n')[0]
        for line in text.split('\n')[1:]:
            originalTabs = line.count('\t') * '\t'
            lineAsList = line.strip().split()
            if (lineAsList[0] == 'if' or lineAsList[0] == 'else:'):
                textWithReturns = textWithReturns + '\n' + originalTabs + ' '.join(lineAsList)
            else:
                textWithReturns = textWithReturns + '\n' + originalTabs + 'return ' + ' '.join(lineAsList)
        return textWithReturns

    def createPythonFile(self):
        with codecs.open(self.pythonFileName, 'w', 'utf-8') as o:
            o.writelines(f"#Automatically generated Python file from YAML:{self.transduction_name}\n")
            o.writelines(f"def personal_setup(self):\n")
            o.writelines(f"{self.inputoutput_alphabetPython}\n")
            o.writelines(f"{self.inputLabelFeaturesPython}\n")
            o.writelines(f"{self.copySetPython}\n")
            #TODO incorporate features
            o.writelines(f"\tself.labels_are_input = True\n")
            o.writelines(f"def personal_features(self):\n\treturn\n")


            o.writelines(f"def personal_predicate_setup(self):\n")
            if len(self.predicateListNames) > 0:
                o.writelines(f"{self.predicateListNamePython}\n")
            else:
                o.writelines(f"\treturn\n")

            o.writelines(f"def personal_OutputLabel_Formula(self, label, node):\n")
            o.writelines(f"\tcopy,domain_element = node\n")
            for outputFunPython in self.outputLabelFormulaPythonList:
                o.writelines(f"{outputFunPython}\n")
            o.writelines(f"\treturn False\n")

            o.writelines(f"def personal_Predicate_Formula(self,predicate,node):\n")
            o.writelines(f"\tlevel,domain_element = node\n")
            if len(self.predicateListNames) > 0:
                for predicatePython in self.predicateLogicPython:
                    o.writelines(f"{predicatePython}\n")
                o.writelines(f"\treturn False\n")
            else:
                o.writelines(f"\treturn\n")





