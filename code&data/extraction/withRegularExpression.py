#-*- coding:utf-8 -*-
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
    #patterns = [u'^(\(.*?\))',u'。' '+(\(.*?\))']
    #patterns = [u'^(\(.*?\))',u'。\s*(\(.*?\))',u'(补充报告.*?\s*\(.*?\))']
    patterns = [u'^(\(.*?[\u4e00-\u9fa5]+?.*?\))',u'[。；]\s*(\(.*?[\u4e00-\u9fa5]+?.*?\))',u'(补充报告.*?\s*\(.*?[\u4e00-\u9fa5]+?.*?\))']
    deletePattern = u'G([\d+\-~～]+)S([\d+\-~～]+)'
    #pattern= u'(\(.*?(肝|胆囊|尾状叶).*?\))'
    #pattern="[\('（']"
    for pattern in patterns:
        for i in re.findall(pattern,text):
            #print 111111111,i
            beDeleted = re.search(deletePattern,i)
            #if text.find(i)==0 or text[text.find(i)-1]==' ' or u'肝' in i:
            #if text.find(i)==0 or text[text.find(i)-1]==' ' or u'肝' in i:
            if not beDeleted:
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
        clinical=(';'.join(cl_raw),u'介入')
    else:
        clinical=('NA','NA')
    return clinical

def process_tag(tag):
    tag = tag.replace('VIII',u'Ⅷ').replace('VII',u'Ⅶ').replace('VI',u'Ⅵ').replace('IV',u'Ⅳ').replace('V',u'Ⅴ').replace('III',u'Ⅲ').replace('II',u'Ⅱ').replace('I',u'Ⅰ')
    return tag

def process_raw(raw):
    raw = raw.replace(u'Ⅷ','VIII').replace(u'Ⅶ','VII').replace(u'Ⅵ','VI').replace(u'Ⅳ','IV').replace(u'Ⅴ','V').replace(u'Ⅲ','III').replace(u'Ⅱ','II').replace(u'Ⅰ','I')
    return raw

#3.12 add process the double type 
def process_types(type):
    typeDict = {}
    #if type != 'NA':
    if 'NA' not in type:
        allTypes = type.keys()
        finalTypes = []
        for t in allTypes:
            i = 0
            for y in allTypes:
                if t in y:
                    i += 1
            if i == 1:
                finalTypes.append(t)
        for f_type in finalTypes:
            if u'胆管细胞癌' in f_type:
                if u'腺癌' in finalTypes:
                    finalTypes.remove(u'腺癌')
        for f_type in finalTypes:
            if u'混合型肝癌' in f_type:
                if u'肝细胞肝癌' in finalTypes:
                    finalTypes.remove(u'肝细胞肝癌')
        fj_list = []
        t_raw_text_list = []
        f_raw_text_list = []
        fjReviewFlag = 0
        reviewFlag = 0
        if len(finalTypes) > 1:
            reviewFlag += 1
        for i in finalTypes:
            fj_list.append(type[i]['fenji'])
            fjReviewFlag += type[i]['fjReviewFlag']
            reviewFlag += type[i]['reviewFlag']
            #print 107,i,type[i]['raw_text']
            t_raw_text_list.append(type[i]['raw_text'][0])
            f_raw_text_list.append(type[i]['raw_text'][1])
        types='+'.join(finalTypes)
        levels='+'.join(fj_list)
        t_raw_text='+'.join(t_raw_text_list)
        f_raw_text='+'.join(f_raw_text_list)
        typeDict['cancerType']=(t_raw_text,types,reviewFlag)
        typeDict['cancerFenji']=(f_raw_text,levels,fjReviewFlag)
    else:
        typeDict['cancerType'] = ('NA','NA',type[-1])
        typeDict['cancerFenji'] = ('NA','NA',type[-1])
    return typeDict
        
def buweiextractor(raw_all,tag):
    tag = process_tag(tag)
    raw_buwei = []
    buwei = []
    # add manually review flag
    reviewFlag = 0
    raw_t = tag.replace('(','').replace(')','')
    raw_t = find_index(process_raw(raw_t),raw_all)
    pattern_dict = {u'肝左叶':[u'肝?左叶',u'左(半)?肝'],u'肝右叶':[u'肝?右叶',u'右(半)?肝'],u'肝中叶':[u'肝?中叶'],u'胆囊':[u'胆囊'],u'肝左外叶':[u'肝?左外叶'],u'肝左内叶':[u'肝?左内叶'],
    u'肝右前叶':[u'肝?右前叶'],u'肝右后叶':[u'肝?右后叶'],u'肝左外叶上段':[u'肝?左外叶上段',u'Ⅱ段'],u'肝左外叶下段':[u'肝?左外叶下段',u'Ⅲ段'],u'肝左内叶上部':[u'肝?左内叶上[段部]',u'Ⅳa段'],
    u'肝左内叶下部':[u'肝?左内叶下[段部]',u'Ⅳb段'],u'肝右前叶下段':[u'肝?右前叶下段',u'Ⅴ段'],u'肝右前叶上段':[u'肝?右前叶上段',u'Ⅷ段'],u'肝右后叶下段':[u'肝?右后叶下段',u'Ⅵ段'],u'肝右后叶上段':[u'肝?右后叶上段',u'Ⅶ段'],
    u'肝尾状叶':[u'肝?尾状?叶']}
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
        if len(buwei) > 1:
            reviewFlag += 1
        return (raw_t,','.join(buwei),reviewFlag)
    elif u'肝' in raw_t:
        reviewFlag += 1
        return (raw_t,u'肝',reviewFlag)
    else:
        #raw_t = tag.replace('(','').replace(')','')
        return (raw_t,'NoLiver',reviewFlag)
           
        
def typeextractor(raw_all,text):
    type={}
    reviewFlag = 0
    fjReviewFlag = 0
    pattern_dict={u'肝内胆管细胞癌':[u'肝内胆管(.*?)肿瘤',u'肝内胆管细胞癌',u'周围[性型](.*)胆管癌',u'肝内胆管腺癌'],u'肝细胞肝癌':[u'肝细胞性?肝?癌'],u'胆管细胞癌':[u'胆管细胞癌',u'胆管(来源)?(.*?)腺癌'],u'混合型肝癌':[u'肝细胞胆管细胞混合细胞癌',u'(.*?癌.*?癌.{0,5})混合[型性]',u'混合[型性](.{0,10}癌.*?癌)',u'(.*?癌.{0,5})混合[型性](.*?癌)'],
    u'海绵状血管瘤':[u'海绵状血管瘤'],u'囊肿':[u'囊肿'],u'局灶性结节性增生':[u'局灶性?结节性?增生',u'FNH'],u'肝母细胞癌':[u'肝母细胞癌'],u'癌肉瘤':[u'癌肉瘤'],u'肝细胞腺瘤':[u'肝(细胞)?腺瘤'],u'肝门胆管细胞癌':[u'肝门胆管(细胞)?癌'],u'腺癌':[u'腺癌'],u'介入后':[u'符合介入(术)?后改变'],
    u'高度异型增生结节':[u'高(级别|度)异型增生结节',u'HDN'],u'低度异型增生结节':[u'低(级别|度)异型增生结节',u'LDN'],u'异型增生结节':[u'异型增生结节'],u'上皮样血管平滑肌脂肪瘤':[u'上皮样血管平滑肌脂肪瘤'],u'原发性硬化性胆管炎':[u'原发性硬化性胆管炎']}
    negation=[u'未见',u'没有']
    doubtWordList=[u'不能除外']
    subtypes = {u'透明细胞型':[u'透明细胞(亚)?型']}
    pattern = u'I*[～-]*I+级'
    for key in pattern_dict.keys():
        for pt in pattern_dict[key]:
            raw_t=[]
            have_t=re.search(pt,text)
            #fenji=re.search(pattern,text)
            fenjiList=re.findall(pattern,text)
            fenjiList=list(set(fenjiList))
            if have_t:
                if key == u'胆管细胞癌':
                    reviewFlag += 1
                f_index=text.find(have_t.group(0))
                ne_index=[]
                doubtWord_index=[]
                for ne in negation:
                    ne_index.append(text[f_index-7:f_index].find(ne))
    #3.15 add doubt words 
                for doubtWord in doubtWordList:
                    doubtWord_index.append(text[f_index+len(have_t.group(0)):f_index+len(have_t.group(0))+7].find(doubtWord))
                if list(set(doubtWord_index)) != [-1]:
                    reviewFlag += 1
                    key = u'{key}(可疑)'.format(key=key)
                #raw_input(list(set(ne_index)))
                if list(set(ne_index)) == [-1]:
                    #raw_input('wu')
                    #if fenji and text.find(have_t.group(0))-text.find(fenji.group(0)) < 12:
                    if fenjiList:
                        if len(fenjiList) > 1:
                            fjReviewFlag  += 1
                        #raw_input(text.find(have_t.group(0)))
                        #raw_input(text.find(fenji.group(0)))
                        f_fenjiList = []
                        f_fenjiRaw_text = []
                        for fenji in fenjiList:
                            if text.find(have_t.group(0))-text.find(fenji) < 12: 
                                #fenji_i = fenji.group(0).replace(u'～',u'-').replace(u'级','')
                                fenjiRaw_text = find_index(fenji,raw_all)
                                fenji_i = fenji.replace(u'～',u'-').replace(u'级','')
                                fenji_i = fenji_i.replace('III','Ⅲ').replace('II','Ⅱ').replace('I','Ⅰ')
                                f_fenjiList.append(fenji_i)
                                f_fenjiRaw_text.append(fenjiRaw_text)
                            else:
                                f_fenjiList.append('NA')
                                f_fenjiRaw_text.append('NA')
                        #3.12 change type dict form
                        #type[key] = fenji_i.replace('III','Ⅲ').replace('II','Ⅱ').replace('I','Ⅰ')
                        type[key] = {}
                        #type[key]['fenji'] = fenji_i.replace('III','Ⅲ').replace('II','Ⅱ').replace('I','Ⅰ')
                        #raw_input(f_fenjiList)
                        type[key]['fenji'] = '+'.join(f_fenjiList)
                            #raw_input(find_index(have_t.group(),raw_all))
                        raw_t.append(find_index(have_t.group(),raw_all))
                        raw_t.append(' '.join(f_fenjiRaw_text))
                        type[key]['raw_text'] = raw_t
                        type[key]['reviewFlag'] = reviewFlag
                        type[key]['fjReviewFlag'] = fjReviewFlag
                    else:
                        type[key] = {}
                        type[key]['fenji'] = 'NA'
                        raw_t.append(find_index(have_t.group(),raw_all))
                        raw_t.append('NA')
                        type[key]['raw_text'] = raw_t
                        type[key]['reviewFlag'] = reviewFlag
                        type[key]['fjReviewFlag'] = fjReviewFlag
    if u'肝细胞肝癌' in type :
        for key in subtypes.keys():
            for subtype in subtypes[key]:
                is_subtype = re.search(subtype,text)
                if is_subtype:
                    keyName = u'肝细胞肝癌({cellSubtype})'.format(cellSubtype=key)
                    subtypeRaw_text = find_index(is_subtype.group(),raw_all)
                    type[keyName] = {}
                    type[keyName]['fenji'] = type[u'肝细胞肝癌']['fenji']
                    type[keyName]['raw_text'] = [type[u'肝细胞肝癌']['raw_text'][0]+subtypeRaw_text,type[u'肝细胞肝癌']['raw_text'][1]]
                    type[keyName]['reviewFlag'] = type[u'肝细胞肝癌']['reviewFlag']+1
                    type[keyName]['fjReviewFlag'] = type[u'肝细胞肝癌']['fjReviewFlag']
                    type.pop(u'肝细胞肝癌')
    if type != {}:
        if u'肝细胞肝癌' in type and u'胆管细胞癌' in type:
            reviewFlag += 1
            fj=[]
            for i in [u'肝细胞肝癌',u'胆管细胞癌']:
                if type[i]['fenji'] not in fj and type[i]['fenji'] != 'NA':
                    fj.append(type[i]['fenji'])
            if len(fj)== 0 :
                return {u'混合型肝癌':{'fjReviewFlag':fjReviewFlag,'reviewFlag':reviewFlag,'fenji':'NA','raw_text':[type[u'肝细胞肝癌']['raw_text'][0]+type[u'胆管细胞癌']['raw_text'][0],type[u'肝细胞肝癌']['raw_text'][1]+type[u'胆管细胞癌']['raw_text'][1]]}}
            elif len(fj) == 1:
                return {u'混合型肝癌':{'fjReviewFlag':fjReviewFlag,'reviewFlag':reviewFlag,'fenji':fj[0],'raw_text':[type[u'肝细胞肝癌']['raw_text'][0]+type[u'胆管细胞癌']['raw_text'][0],type[u'肝细胞肝癌']['raw_text'][1]+type[u'胆管细胞癌']['raw_text'][1]]}}
            elif len(fj) == 2:
                fjReviewFlag += 1
                return {u'混合型肝癌':{'fjReviewFlag':fjReviewFlag,'reviewFlag':reviewFlag,'fenji':processfj(fj),'raw_text':[type[u'肝细胞肝癌']['raw_text'][0]+type[u'胆管细胞癌']['raw_text'][0],type[u'肝细胞肝癌']['raw_text'][1]+type[u'胆管细胞癌']['raw_text'][1]]}}
        else:
            return type
    else:
        # 当没有搜寻到定义的细胞类型时，需要reviewFlag
        reviewFlag += 1
        return 'NA',reviewFlag

def fenjiextractor(text):
    pattern = u'I*[～-]*I+级'
    fenji=re.search(pattern,text)
    if fenji:
        return fenji.group(0).replace(u'～',u'-').replace(u'级','')
    else:
        return 'NA'
    
def aishuanextractor(raw_all,text):
    #pt1=u'[(脉管)(门脉系)]内?可?[见有(疑有)]癌栓'
    pts1=[u'(脉管(及胆管)?|门脉系)内?(可|易)?疑?(见|有)(.*)癌栓',u'(脉管(及胆管)?|门脉系)内?癌栓(可|易)?疑?(见|有)',u'(脉管(及胆管)?|门脉系)内?(可|易)疑?癌栓']
    pts2=[u'(脉管|门脉系|切片)内?未见(.*)癌栓',u'未见(脉管|门脉系|切片)内?(.*)癌栓']
    yi_list = [u'疑']
    reviewFlag = 0
    for pt1 in pts1:
        if re.search(pt1,text):
            for yi in yi_list:
                if yi in re.search(pt1,text).group():
                    reviewFlag += 1
                    return (find_index(re.search(pt1,text).group(),raw_all),'true/false',reviewFlag)
                else:
                    return (find_index(re.search(pt1,text).group(),raw_all),'true',reviewFlag)
        #print re.search(pt1,text).group()
    for pt2 in pts2:
        if re.search(pt2,text):
            #print re.search(pt2,text).group()
            return (find_index(re.search(pt2,text).group(),raw_all),'false',reviewFlag)
    return ('NA','false',reviewFlag)

def qieyuanextractor(raw_all,text):
    pt1 = u'肝?切缘.{0,3}未见(癌|肿瘤)(组织)?累及'
    pt2 = u'肝?切缘.{0,3}见(癌|肿瘤)(组织)?累及'
    reviewFlag = 0
    if re.search(pt1,text):
        return (find_index(re.search(pt1,text).group(),raw_all),'false')
    elif re.search(pt2,text):
        return (find_index(re.search(pt2,text).group(),raw_all),'true')
    else:
        return ('NA','NA',reviewFlag)
        
def zhuanyiextractor(raw_all,text):
    pattern1s = [u'(符合|考虑|倾向)(.{1,15}?[瘤癌]).{,2}转移',u'(符合|考虑|倾向)?转移性(.{1,15}?[瘤癌])',u'^()(.{1,10}?[瘤癌]).{,2}转移']
    pattern2 = u'.+(肿?瘤|癌)'
    jpbuwei = [u'肠',u'肾',u'乳腺',u'肺',u'胆囊',u'胃',u'卵巢',u'骨']
    negationWordList = [u'未见',u'没有']
    reviewFlag = 0
    for pattern1 in pattern1s:
        zhuanyi_long = re.search(pattern1,text)
        #print 'tumorT',zhuanyi_long.group()
        if zhuanyi_long:
        #add negation words list
            for word in negationWordList:
                if word in zhuanyi_long.group():
                    reviewFlag += 1
                    return 'NA',reviewFlag
            zhuanyi_dict={}
            #raw_input(re.findall(pattern1,text))
            zhuanyi1 = re.search(pattern2,re.findall(pattern1,text)[0][1])
            if zhuanyi1:
                #raw_input(1111)
                zhuanyi = re.search(pattern2,re.findall(pattern1,text)[0][1]).group(0)
                if u'肝' in zhuanyi:
                    reviewFlag += 1
                    #return 'NA',reviewFlag
            else:
                reviewFlag += 1
                zhuanyi = 'NA'
            zhuanyi_dict['raw_text'] = find_index(zhuanyi_long.group(),raw_all)
            zhuanyi_dict['ai'] = zhuanyi
            zhuanyi_dict['fj'] = fenjiextractor(zhuanyi_long.group())
            zhuanyi_dict['reviewFlag'] = reviewFlag
            for i in jpbuwei:
                if i in zhuanyi:
                    zhuanyi_dict['bw'] = i
                    return zhuanyi_dict
            zhuanyi_dict['bw'] = 'NA'
            zhuanyi_dict['reviewFlag'] += 1
            return zhuanyi_dict
    return 'NA',reviewFlag

def GSextractor(raw_all,text):
    pattern ,pattern0 ,pattern1 ,pattern2= u'[Gg]([\d+\-~～]+)[Ss]([\d+e?\-~～]+)',u'[Ss]([\d+e?\-~～]+)[Gg]([\d+\-~～]+)',u'周围肝.*[Gg]([\d+\-~～]+)',u'周围肝.*[Ss]([\d+e?\-~～]+)'
    patternd = u'\de?'
    GStuple=['','']
    reviewFlag = 0
    if re.search(pattern,text) or re.search(pattern0,text):
        if re.search(pattern,text): 
            Graw,Sraw=re.search(pattern,text).group(1),re.search(pattern,text).group(2)
            raw_text=find_index(re.search(pattern,text).group(),raw_all)
        else:
            Sraw,Graw=re.search(pattern0,text).group(1),re.search(pattern0,text).group(2)
            raw_text=find_index(re.search(pattern0,text).group(),raw_all)
        GStuple.append(raw_text)
        GStuple[0],GStuple[1]=re.findall(patternd,Graw),re.findall(patternd,Sraw)
        if len(GStuple[0])!=0:GStuple[0]='-'.join(GStuple[0])
        if len(GStuple[1])!=0:GStuple[1]='-'.join(GStuple[1])
        GStuple.append(reviewFlag)
        return GStuple 
    elif re.search(pattern1,text) or re.search(pattern2,text):
        if re.search(pattern1,text):
            Graw=re.search(pattern1,text).group(1)
            raw_text=find_index(re.search(pattern1,text).group(),raw_all)
            GStuple[0],GStuple[1]=re.findall(patternd,Graw),'NA'
        else:
            Sraw=re.search(pattern2,text).group(1)
            raw_text=find_index(re.search(pattern2,text).group(),raw_all)
            GStuple[0],GStuple[1]='NA',re.findall(patternd,Sraw)
        GStuple.append(raw_text)
        if len(GStuple[0])!=0 and GStuple[0]!='NA':GStuple[0]='-'.join(GStuple[0])
        if len(GStuple[1])!=0 and GStuple[1]!='NA':GStuple[1]='-'.join(GStuple[1])
        GStuple.append(reviewFlag)
        return GStuple 
    else:
        return ['NA','NA','NA',reviewFlag]
        
def process_bingli(i):
    #print i
    i = str(i)
    i = i.replace(u'（','(').replace(u'）',')')
    tags = split_text(i)
    #print tags
    ###2016.12.12 delete "liver" have to be in tags 
    #if u'肝' or u'尾状叶' in ''.join(tags) and u'供肝' not in ''.join(tags):
    #print 11111111111
    baogao_dict={}
    baogao_dict['raw'] = i
    baogao_dict['clinical'] = clinicalextractor(i)
    baogao_dict['notes'] = []
    reports = {}
    for j in range(len(tags)):
        if j < len(tags)-1:
            reports[tags[j]] = i[i.find(tags[j])+len(tags[j]):i.find(tags[j+1])]
        else:
            #raw_input(tags[j])
            reports[tags[j]] = i[i.find(tags[j])+len(tags[j]):]
    for report in reports:
        #3.15 add delete no liver
        ###2016.12.12 not have to have "liver"
        #if u'肝' not in report and u'尾状叶' not in report and u'胆囊' not in report:
            #continue
        reports[report] = preprocess(reports[report])
        #print 1111,reports[report]
        part={}
        part['type']={}
        type = typeextractor(i,reports[report])
        #print type
        typeDict = process_types(type)
        part['type']['type'] = typeDict['cancerType']
        part['type']['fenji'] = typeDict['cancerFenji']
        part['jiepo'] = buweiextractor(i,report)
        #part['type'] = typeextractor(reports[report])
        #part['fenji'] = fenjiextractor(reports[report])
        #print 315,reports[report],315,i
        part['zhuanyi'] = zhuanyiextractor(i,reports[report])
        part['aishuan'] = aishuanextractor(i,reports[report])
        part['qieyuan'] = qieyuanextractor(i,reports[report])
        #if part['zhuanyi'] != 'NA':
        if 'NA' not in part['zhuanyi']:
            part['zhuanyiOrNot'] = (part['zhuanyi']['raw_text'],'true',part['zhuanyi']['reviewFlag'])
            part['zhuanyiTumorLocation'] = (part['zhuanyi']['raw_text'],part['zhuanyi']['bw'],part['zhuanyi']['reviewFlag'])
            part['zhuanyiTumorType'] = (part['zhuanyi']['raw_text'],part['zhuanyi']['ai'],part['zhuanyi']['reviewFlag'])
            part.pop('zhuanyi')
            #part['type']['type'] = ('NA','NA')
            #part['type']['fenji'] = ('NA','NA')
        else:
            part['zhuanyiOrNot'] = ('NA','false',part['zhuanyi'][-1])
            part.pop('zhuanyi')
        part['tomorType'] = part['type']['type']
        part['tomorLevel'] = part['type']['fenji']
        part.pop('type')
        GS = GSextractor(i,reports[report])
        part['Gscore'] = (GS[2],GS[0],GS[-1])
        part['Sscore'] = (GS[2],GS[1],GS[-1])
        baogao_dict['notes'].append(part)
        #print baogao_dict
    return baogao_dict

def main():
    #2016.3.2 test preprocess
    #text = u'（肝右后叶）腺癌，分化II～III级，伴地图样坏死，脉管内易见癌栓。结合病史及免疫组化结果，符合肠腺癌肝转移。  周围肝组织未见结节性肝硬化（G1S1）。  免疫组化(2014-N7886) 2号蜡块:AFP(-),Hepa(部分+),CK7(部分+),CK19(++),KI67(80%阳性),CDX-2(+),CK20(+),VIM(-)，Villin(+)。'
    #text = u'（肝右叶）结节内增生的肝细胞呈细索状排列，局灶区呈更多层肝细胞，部分肝细胞核异型CD34示血窦丰富，网染示网状纤维结构存在，结节中可见小胆管、血管，炎症细胞浸润伴灶性坏死，考虑为腺瘤样增生结节，小灶区高分化肝细胞肝癌不能除外。周围肝组织结节性肝硬化伴大细胞不典型增生。汇管区较多炎症细胞浸润。(G2S4)建议临床密切随访。'
    text = u'（胸椎）转移癌，结合病史及免疫组化结果，符合肝细胞癌骨转移。免疫组化（2015-N2656)：15S05665-002：AFP(-),Hepa(++),CK广(50%+),Vim(-),CD34(血管较丰富),CK7(-),CK19(-),GPC3(20%+),Syn(-),CHG(-),CD56(-),Ki-67(8%阳性),CD10(70%+-++)'
    text1 = u'（左半肝)结合病史及免疫组织化学检查结果，符合乳腺癌肝转移，周围肝组织未见结节性肝硬化。  胆囊慢性炎。  免疫组化(2012-N0819):ER(20%弱+),PR(部分+/-),CerbB2(50%+～++),Hepa(-),CK7(++),CK19(+),KI67(30%+),P120(+),AFP(-),CD56(-),S100(-)。'
    #print 22222,zhuanyiextractor(u'腺癌伴坏死(6灶)，结合病史，符合转移性腺癌。',u'腺癌伴坏死(6灶)，结合病史，符合转移性腺癌。')
    print process_bingli(text)
if __name__ == '__main__':
    main()
