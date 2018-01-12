#-*- encoding:utf-8 -*-
import iCMC
INI_FILE_PATH = 'APPs/Pathology/development.ini'
booleanList = iCMC.getOptionFromSectionOfINIFile(INI_FILE_PATH,'dataType','boolean')[1].split(',')
cdList = iCMC.getOptionFromSectionOfINIFile(INI_FILE_PATH,'dataType','cd')[1].split(',')
codeSystem = iCMC.getOptionFromSectionOfINIFile(INI_FILE_PATH,'main','codeSystem')[1]
codeSystemName = iCMC.getOptionFromSectionOfINIFile(INI_FILE_PATH,'main','codeSystemName')[1]
#booleanList = ['aishuan','qieyuan']
#cdList = ['jiepo']
#codeSystem = ''
#codeSystemName = ''

def getCode(key,value):
    code = {}
    code['entity'] = 'entity'
    code['feature'] = 'feature'
    code['value'] = 'value'
    return code
def getDisplayName(key,value):
    displayName = {}
    displayName['entity'] = u'标本'
    displayName['feature'] = iCMC.getOptionFromSectionOfINIFile(INI_FILE_PATH,'norName',key)[1]
    displayName['value'] = 'value'
    return displayName
def pathologyParser(pathologyContent,parseEnzyme = 'bingli'):
    modPath = 'APPs.Pathology.{enzyme}'.format(enzyme=parseEnzyme) 
    mod = __import__(modPath,{},{},parseEnzyme)
    print mod
    pathologyReportParser = getattr(mod,'process_bingli')
    #pathologyReportParser = theClass()
    inputData = pathologyReportParser(pathologyContent)
    outputData = []
    for part in inputData['notes']:
        partData=[]
        for key in part.keys():
            if key in booleanList:
                dataDict = {}
                dataDict['type'] = 'boolean'
                dataDict['norName'] = iCMC.getOptionFromSectionOfINIFile(INI_FILE_PATH,'norName',key)[1]
                dataDict['value'] = {}
                dataDict['code'] = {}
                dataDict['originalText'] = {}
                dataDict['value']['value'] = part[key][1]
                #2016.3.19 add review flag
                dataDict['value']['reviewFlag'] = part[key][-1]
                dataDict['code']['code'] = getCode(key,part[key][1])
                dataDict['code']['displayName'] = getDisplayName(key,part[key][1])
                dataDict['originalText']['value'] = part[key][0]
                partData.append(dataDict)
                #outputData.append(dataDict)
            if key in cdList:
                dataDict = {}
                dataDict['type'] = 'cd'
                dataDict['norName'] = iCMC.getOptionFromSectionOfINIFile(INI_FILE_PATH,'norName',key)[1]
                dataDict['value'] = {}
                dataDict['code'] = {}
                dataDict['originalText'] = {}
                dataDict['value']['code'] = ''
                #2016.3.19 add review flag
                dataDict['value']['reviewFlag'] = part[key][-1]
                dataDict['value']['displayName'] = part[key][1]
                dataDict['value']['codeSystem'] = codeSystem
                dataDict['value']['codeSystemName'] = codeSystemName
                dataDict['code']['code'] = getCode(key,part[key][1])
                dataDict['code']['displayName'] = getDisplayName(key,part[key][1])
                dataDict['originalText']['value'] = part[key][0]
                partData.append(dataDict)
                #outputData.append(dataDict)
        outputData.append(partData)
    return outputData
def main():
    #text = u'(胆管栓子)镜下为肝细胞肝癌组织。 (胆囊)慢性炎。 (胆管旁淋巴结)镜下为癌结节3枚。（胆道栓子）肝细胞肝癌。'
    #print pathologyParser(text,'withRegularExpression')
    print __import__('withRegularExpression')
if __name__ =='__main__':
    main()