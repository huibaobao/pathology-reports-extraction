#-*- coding:utf-8 -*-
import xlrd
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from mako.template import Template

def preprocess(text):
    text=text.replace(u'（','(').replace(u'）',')')
    pattern1 = u'酶标\(.*?\w+-\w+\)'
    if re.search(pattern1,text):
        index1 = re.search(pattern1,text).span()[0]
        text = text[0:index1]
    pattern2 = u'免疫组化\(.*?\w+-\w+\)'
    if re.search(pattern2,text):
        index1 = re.search(pattern2,text).span()[0]
        text = text[0:index1]
    return text

def process_tag(tag):
    tag = tag.replace('VIII','Ⅷ').replace('VII','Ⅶ').replace('VI','Ⅵ').replace('IV','Ⅳ').replace('V','Ⅴ').replace('III','Ⅲ').replace('II','Ⅱ').replace('I','Ⅰ')
    
def find_index(raw_text,text):
    s_index=text.find(raw_text)
    e_index=s_index+len(raw_text)-1
    result = '"'+raw_text+'" '+'1:'+str(s_index)+' 1:'+str(e_index)
    return result
    
def processfj(fenji):
    if u'III' in fenji:
        return u'III'
    else:
        for i in fenji:
            if u'III' in i:
                return i
        if u'II' in fenji:
            return u'II'
        else:
            for i in fenji:
                if u'II' in i:
                    return i
            return u'I'
            
def split_text(text):
    split_tags=[]
    pattern= u'(\(.*?\))'
    #pattern="[\('（']"
    for i in re.findall(pattern,text):
        if text.find(i)==0 or text[text.find(i)-1]==' ':
                if i not in split_tags:
                    split_tags.append(i)
    return split_tags

def clinicalextractor(text):
    cl_raw = []
    cl_key = []
    clinical=()
    pattern_dict = {u'介入':[u'符合.*?介入术',u'符合.*?介入治疗'],u'穿刺':[u'(占位)?穿刺(活检)?']}
    for key in pattern_dict.keys():
        for pattern in pattern_dict[key]:
            have_t=re.search(pattern,text)
            if have_t:
                cl_key.append(key)
                cl_raw.append(find_index(have_t.group(),text))
    if u'介入' in cl_key and u'穿刺' in cl_key:
        clinical=(u'介入',';'.join(cl_raw))
    if clinical != ():
        return clinical
    else:
        return 'NA'

def process_tag(tag):
    tag = tag.replace('VIII',u'Ⅷ').replace('VII',u'Ⅶ').replace('VI',u'Ⅵ').replace('IV',u'Ⅳ').replace('V',u'Ⅴ').replace('III',u'Ⅲ').replace('II',u'Ⅱ').replace('I',u'Ⅰ')
    return tag

def process_raw(raw):
    raw = raw.replace(u'Ⅷ','VIII').replace(u'Ⅶ','VII').replace(u'Ⅵ','VI').replace(u'Ⅳ','IV').replace(u'Ⅴ','V').replace(u'Ⅲ','III').replace(u'Ⅱ','II').replace(u'Ⅰ','I')
    return raw
    
def buweiextractor(raw_all,tag):
    tag = process_tag(tag)
    raw_buwei = []
    buwei = []
    raw_t = tag.replace('(','').replace(')','')
    raw_t = find_index(process_raw(raw_t),raw_all)
    pattern_dict = {u'肝左叶':[u'肝左叶',u'左肝'],u'肝右叶':[u'肝右叶',u'右肝'],u'肝中叶':[u'肝中叶'],u'胆囊':[u'胆囊'],u'肝左外叶':[u'肝?左外叶'],u'肝左内叶':[u'肝?左内叶'],
    u'肝右前叶':[u'肝?右前叶'],u'肝右后叶':[u'肝?右后叶'],u'肝左外叶上段':[u'肝?左外叶上段',u'Ⅱ段'],u'肝左外叶下段':[u'肝?左外叶下段',u'Ⅲ段'],u'肝左内叶上部':[u'肝?左内叶上[段部]',u'Ⅳa段'],
    u'肝左内叶下部':[u'肝?左内叶下[段部]',u'Ⅳb段'],u'肝右前叶下段':[u'肝?右前叶下段',u'Ⅴ段'],u'肝右前叶上段':[u'肝?右前叶上段',u'Ⅷ段'],u'肝右后叶下段':[u'肝?右后叶下段',u'Ⅵ段'],u'肝右后叶上段':[u'肝?右后叶上段',u'Ⅶ段']}
    for key in pattern_dict.keys():
        for pattern in pattern_dict[key]:
            have_t=re.search(pattern,tag)
            if have_t:
                #raw_input(process_raw(have_t.group()))
                raw_buwei.append(find_index(process_raw(have_t.group()),raw_all))
                if key not in buwei:
                    if key != u'胆囊':
                        buwei.append(u'肝-'+key)
                    else:
                        buwei.append(key)
    if buwei != []:
        for bw in buwei:
            for bw2 in buwei:
                if bw[:-1] in bw2[:-1] and len(bw2) > len(bw):
                    buwei.remove(bw)
        #return (','.join(raw_buwei),','.join(buwei))
        return (raw_t,','.join(buwei))
    else:
        #raw_t = tag.replace('(','').replace(')','')
        return (raw_t,u'肝')
           
        
def typeextractor(raw_all,text):
    type={}
    raw_t=[]
    pattern_dict={u'肝内胆管细胞癌':[u'肝内胆管(.*?)肿瘤'],u'胆管腺癌':[u'胆管腺癌'],u'肝细胞肝癌':[u'肝细胞肝癌'],u'胆管细胞癌':[u'胆管细胞癌'],u'混合型肝癌':[u'肝细胞胆管细胞混合细胞癌'],u'海绵状血管瘤':[u'海绵状血管瘤'],u'囊肿':[u'囊肿'],u'局灶性结节性增生':[u'局灶性?结节性?增生']}
    negation=[u'未见',u'没有']
    pattern = u'I*[～-]*I+级'
    for key in pattern_dict.keys():
        for pt in pattern_dict[key]:
            have_t=re.search(pt,text)
            fenji=re.search(pattern,text)
            if have_t:
                f_index=text.find(have_t.group(0))
                ne_index=[]
                for ne in negation:
                    ne_index.append(text[f_index-7:f_index].find(ne))
                #raw_input(list(set(ne_index)))
                if list(set(ne_index)) == [-1]:
                    #raw_input('wu')
                    if fenji and text.find(have_t.group(0))-text.find(fenji.group(0)) < 12:
                        fenji_i = fenji.group(0).replace(u'～',u'-').replace(u'级','')
                        type[key] = fenji_i.replace('III','Ⅲ').replace('II','Ⅱ').replace('I','Ⅰ')
                        raw_t.append(find_index(have_t.group(),raw_all))
                        raw_t.append(find_index(fenji.group(),raw_all))
                        type['raw_text'] = raw_t
                    else:
                        type[key] = 'NA'
                        raw_t.append(find_index(have_t.group(),raw_all))
                        type['raw_text'] = raw_t
    if type != {}:
        if u'肝细胞肝癌' in type and u'胆管细胞癌' in type:
            fj=[]
            for i in [u'肝细胞肝癌',u'胆管细胞癌']:
                if type[i] not in fj and type[i] != 'NA':
                    fj.append(type[i])
            if len(fj)== 0 :
                return {u'混合型肝癌':'NA','raw_text':raw_t}
            elif len(fj) == 1:
                return {u'混合型肝癌':fj[0],'raw_text':raw_t}
            elif len(fj) == 2:
                return {u'混合型肝癌':processfj(fj),'raw_text':raw_t}
        else:
            return type
    else:
        return 'NA'

def fenjiextractor(text):
    pattern = u'I*[～-]*I+级'
    fenji=re.search(pattern,text)
    if fenji:
        return fenji.group(0).replace(u'～',u'-').replace(u'级','')
    else:
        return 'NA'
    
def aishuanextractor(raw_all,text):
    #pt1=u'[(脉管)(门脉系)]内?可?[见有(疑有)]癌栓'
    pt1=u'(脉管|门脉系)内?可?(见|疑?有)癌栓'
    pt2=u'(脉管|门脉系)内?未见癌栓'
    if re.search(pt1,text):
        print re.search(pt1,text).group()
        return (find_index(re.search(pt1,text).group(),raw_all),'true')
    elif re.search(pt2,text):
        print re.search(pt2,text).group()
        return (find_index(re.search(pt2,text).group(),raw_all),'false')
    else:
        return 'NA'

def qieyuanextractor(raw_all,text):
    pt1 = u'肝?切缘.{0,3}未见(癌|肿瘤)(组织)?累及'
    pt2 = u'肝?切缘.{0,3}见(癌|肿瘤)(组织)?累及'
    if re.search(pt1,text):
        return (find_index(re.search(pt1,text).group(),raw_all),'false')
    elif re.search(pt2,text):
        return (find_index(re.search(pt2,text).group(),raw_all),'true')
    else:
        return 'NA'
        
def zhuanyiextractor(raw_all,text):
    pattern1 = u'(符合|考虑|倾向)(.{1,15}?)肝?转移'
    pattern2 = u'.+癌'
    jpbuwei = [u'肠',u'肾',u'乳腺',u'肺',u'胆囊',u'胃']
    zhuanyi_long = re.search(pattern1,text)
    if zhuanyi_long:
        zhuanyi_dict={}
        #raw_input(re.findall(pattern1,text))
        zhuanyi = re.search(pattern2,re.findall(pattern1,text)[0][1]).group(0)
        zhuanyi_dict['raw_text'] = find_index(zhuanyi_long.group(),raw_all)
        zhuanyi_dict['ai'] = zhuanyi
        zhuanyi_dict['fj'] = fenjiextractor(zhuanyi_long.group())
        for i in jpbuwei:
            if i in zhuanyi:
                zhuanyi_dict['bw'] = i
                return zhuanyi_dict
        zhuanyi_dict['bw'] = 'NA'
        return zhuanyi_dict
    else:
        return 'NA'
        
def process_bingli(i):
    print i
    i = preprocess(i)
    tags = split_text(i)
    for tag in tags:
        if u'肝' not in tag and u'胆囊' not in tag:
            tags.remove(tag)
    if u'肝' in ''.join(tags) and u'供肝' not in ''.join(tags) and u'巨检' not in i:
        baogao_dict={}
        baogao_dict['raw'] = i
        baogao_dict['clinical'] = clinicalextractor(i)
        baogao_dict['notes'] = []
        reports = {}
        for j in range(len(tags)):
            if j < len(tags)-1:
                reports[tags[j]] = i[i.find(tags[j])+len(tags[j]):i.find(tags[j+1])]
            else:
                reports[tags[j]] = i[i.find(tags[j])+len(tags[j]):]
        for report in reports:
            part={}
            part['type']={}
            type = typeextractor(i,reports[report])
            print type
            if type != 'NA':
                k_1=type.keys()
                k_1.remove('raw_text')
                k=''.join(k_1)
                part['type']['type']=(type['raw_text'][0],k)
                if type[k] != 'NA':
                    part['type']['fenji']=(type['raw_text'][1],type[k])
                else:
                    part['type']['fenji']=('NA',type[k])
            print reports[report]
            part['jiepo'] = buweiextractor(i,report)
            #part['type'] = typeextractor(reports[report])
            #part['fenji'] = fenjiextractor(reports[report])
            part['zhuanyi'] = zhuanyiextractor(i,reports[report])
            part['aishuan'] = aishuanextractor(i,reports[report])
            part['qieyuan'] = qieyuanextractor(i,reports[report])
            if part['zhuanyi'] == u'是':
                part['type']['type'] = 'NA'
                part['type']['fenji'] = 'NA'
            baogao_dict['notes'].append(part)
            print baogao_dict
        return baogao_dict

def main():
    #2016.3.2 test preprocess
    text = u'（肝右后叶）腺癌，分化II～III级，伴地图样坏死，脉管内见癌栓。结合病史及免疫组化结果，符合肠腺癌肝转移。  周围肝组织未见结节性肝硬化（G1S1）。  免疫组化(2014-N7886) 2号蜡块:AFP(-),Hepa(部分+),CK7(部分+),CK19(++),KI67(80%阳性),CDX-2(+),CK20(+),VIM(-)，Villin(+)。'
    print preprocess(text)
    print process_bingli(text)
if __name__ == '__main__':
    main()
