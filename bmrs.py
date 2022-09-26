import sys

from logicCompiler import logicCompilation
from lispConverter import lispConversion

parameter = sys.argv[1] #
if parameter == 'convert':
    yamlfile = sys.argv[2]
    if len(sys.argv) >3:
        pythonFileName=sys.argv[3]
        conversionObj = lispConversion(yamlfile, pythonFileName)
    else:
        pythonFileName = yamlfile[:-4] + '.py'
        conversionObj = lispConversion(yamlfile, pythonFileName)
elif parameter == 'run':
    file =  sys.argv[2]
    word =  sys.argv[3]
    word_type = 'string'
    # TODO: incorporate freedom to pick word models
    if file[-3:] == '.py':
        runningObj = logicCompilation(word,word_type, file)
        print(f"Output:{runningObj.outputString}")
    else:
        pythonFileName = file[:-4] + '.py'
        conversionObj = lispConversion(file, pythonFileName)
        runningObj = logicCompilation(word,word_type, pythonFileName)
        print(f"Output:{runningObj.outputString}")







