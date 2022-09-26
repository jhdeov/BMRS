import sys

from logicCompiler import logicCompilation
from yamlConverter import yamlConversion

parameter = sys.argv[1] #
if parameter == 'convert':
    yamlfile = sys.argv[2]
    if len(sys.argv) >3:
        pythonFileName=sys.argv[3]
        conversionObj = yamlConversion(yamlfile, pythonFileName)
    else:
        pythonFileName = yamlfile[:-4] + '.py'
        conversionObj = yamlConversion(yamlfile, pythonFileName)
elif parameter == 'run':
    file =  sys.argv[2]
    word =  sys.argv[3]
    if file[-3:] == '.py':
        runningObj = logicCompilation(word, file)
        print(f"Output:{runningObj.outputString}")
    else:
        pythonFileName = file[:-4] + '.py'
        conversionObj = yamlConversion(file, pythonFileName)
        runningObj = logicCompilation(word, pythonFileName)
        print(f"Output:{runningObj.outputString}")

#
# outFileArmToLatin = "" + inFile[:-4] + "_ArmToLatin.txt"  ##outfile.txt"##.inFile[:-3] + "txt"
# outFileLatinToArm = "" + inFile[:-4] + "_LatinToArm.txt"
#
# word = 'HLHLH'
#
# bmrs = 'Formulas.IterStressHixk'
#
# process=Input(word,bmrs)








