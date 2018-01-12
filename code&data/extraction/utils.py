#encoding:utf8
import re
import json,yaml
def normalize_text(text):
    text = re.sub('\s+',' ',text)
    text = re.sub(u'　', ' ',text)
    pattern2 = u'免疫组化\(.*?\w+-\w+\)'
    if re.search(pattern2, text):
        index1 = re.search(pattern2, text).span()[0]
        text = text[0:index1]
    normal_punc_dict = {':':u'：', ';':u'；', '(':u'（', ')':u'）', '?':u'？', ',':u'，', u'—':'-'}
    for punc in normal_punc_dict:
        text = text.replace(punc,normal_punc_dict[punc])
    return text

def segSectionWithRE(text, element_dict):
    # elementDict = {u'超声号':u'超声号', u'报告日期':u'报告日期', u'检查结论':u'检查结论', u'影像所见':u'影像所见'}
    elementDict = element_dict
    segDict = {}
    newStr = text + 'ASegNote'
    #newStr = text.replace('\n','') + 'ASegNote'
    #print newStr
    for secName in elementDict:
        secNamePattern = elementDict[secName]+u'(\s+)?(：|:)'
        newStr = re.sub(secNamePattern,'ASegNote'+secName+u'：',newStr)
    for secName in elementDict:
        RE_PATTERN_ONESECTION_NAME = secName+u'：'+'(.*?)ASegNote'
        sectionStrList = re.compile(RE_PATTERN_ONESECTION_NAME).findall(newStr)
        segDict[secName] = ''.join(sectionStrList).strip()
    return segDict

def sample_json_2_yaml_knol(jsonFile):
    lines = open(jsonFile,'r').readlines()
    knolDict = json.loads(''.join(lines))
    knolDictforClips = {}
    for key in knolDict:
        label = key
        knolDictforClips[label]={}
        for indicator in knolDict[key].keys():
            #text=i[1].decode('utf8')
            text = indicator
            f_dict={}
            f_dict['keywords']=[]
            for keyword in knolDict[key][indicator]['keywords']:
                if type(keyword) == list:
                    print tuple(keyword)
                    f_dict['keywords'].append(tuple(keyword))
                else:
                    f_dict['keywords'].append((keyword,))
            if text == u'否' or text == u'无':
                f_dict['negation'] = []
            else:
                f_dict['negation'] = [u'否认', u'无',u'没有',u'未见',u'不是',u'拒绝',u'未检测',u'未监测']
            if knolDict[key][indicator].has_key('scope'):
                f_dict['scope'] = knolDict[key][indicator]['scope']
            else:
                f_dict['scope'] = [10,10]
            if knolDict[key][indicator].has_key('valuePattern'):
                f_dict['value_type'] = True
                f_dict['value_expression'] = knolDict[key][indicator]['valuePattern']
                f_dict['value_unit'] = knolDict[key][indicator]['unit']
            else:
                f_dict['value_type'] = False
                f_dict['value_expression'] = []
                f_dict['value_unit'] = []
            #f_dict['value_includeRange'] = {'logic': '','max': [],'min': []}
            knolDictforClips[label][text] = f_dict
    return knolDictforClips
    
def main():
    jsonFile = 'knol/form_knol.json'
    yamlPath = 'test.yaml'
    knolDictforClips = sample_json_2_yaml_knol(jsonFile)
    f=open(yamlPath,'w')
    #allow_unicode=True is very important
    yaml.dump(knolDictforClips,f,allow_unicode=True)
    f.close()
if __name__ == '__main__':
    main()