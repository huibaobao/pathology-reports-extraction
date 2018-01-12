#-*- coding:utf-8 -*-
from utils import normalize_text, segSectionWithRE
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def split_structured_text(text):
    result_dict = {}
    if u'预后 指标' in text:
        raw_text = text.split(u'预后 指标')[0].replace(' ', '')
        s_text = text.split(u'预后 指标')[1].strip()
        if u'淋 巴 管' in s_text:
            text_list = s_text.split(u'淋 巴 管')
            s_text_1 = text_list[0]
            s_text_2 = text_list[1]
            print s_text_1, s_text_2
        else:
            index = s_text.find(u'MVI提示风险分级')
            s_text_1 = s_text[:index]
            s_text_2 = s_text[index:]
    else:
        return text.replace(' ', ''), result_dict
    element_dict_1 = {u'术式':u'术式', u'单发肿瘤':u'单发肿瘤', u'多发肿瘤':u'多发肿瘤', u'肉眼类型':u'肉眼类型', u'组织类型':u'组织类型', u'分级':u'分级', u'卫星灶':u'卫星灶', u'可见脉管侵犯':u'脉管侵犯：（巨检／手术所见）', u'微脉管侵犯':u'微脉管侵犯（显微镜下所见）'}
    element_dict_2 = {u'MVI提示风险分级':u'MVI提示风险分级', u'小胆管癌栓':u'小胆管癌栓', u'肝硬化':u'肝硬化', u'胆管侵犯':u'胆管侵犯', u'胆囊侵犯':u'胆囊侵犯', u'周围神经侵犯':u'周围神经侵犯', u'邻近组织侵犯':u'邻近组织侵犯', u'切除面':u'切除面', u'肝被膜':u'肝被膜', u'远处转移':u'远处转移', u'癌周围肝组织':u'癌周围肝组织', u'另送膈肌':u'另送膈肌', u'肝炎':u'肝炎', u'淋巴结':u'淋巴结'}
    dict_1 = segSectionWithRE(s_text_1, element_dict_1)
    dict_2 = segSectionWithRE(s_text_2, element_dict_2)
    result_dict = dict(dict_1, **dict_2)
    return raw_text, result_dict



def main():
    text = u'(肝右叶) 肝细胞肝癌(2灶），II级，伴坏死，肝切缘未见癌累及。巨检0.5cm结节，镜下为低级别异型增生结节。 周围肝组织结节性肝硬化(G2S4）。                 预后 指标     术式:部分肝 多发肿瘤：数目(N=2),大小(最大者直径6cm，最小者直径4cm)  肉眼类型：多结节型有包膜 组织类型:肝细胞癌(细梁型,粗梁型,团片型)  分级:肝细胞癌(II) 卫星灶:无  脉管侵犯:(巨检／手术所见）：无 微脉管侵犯(显微镜下所见）：有　                累及脉管数量  累犯脉管最远距离(mm)  悬浮癌细胞≤50个/＞50个   门脉分支(包括肿瘤包膜)  2  &lt;10     肝静脉分支         肝动脉分支         淋　巴　管                  MVI提示风险分级：　●M1(低危组）,≤5个MVI，且发生于近癌旁肝组织(≤1cm）　             小胆管癌栓:无 肝硬化:有，大小结节混合型  胆管侵犯:无 胆囊侵犯:未知  周围神经侵犯:无 邻近组织侵犯:未知  切除面:未有癌,距肿瘤最近距离2.5cm 淋巴结:无淋巴结  肝被膜:未侵犯 远处转移:未知  癌周围肝组织:肝细胞大、小细胞变 另送膈肌:无  肝炎:有,肝炎程度G2纤维化分期S4  免疫组化(2016-N00653)：16S01550-002：AFP(-),Arg-1(100%+),CD34(血管+),CK19(-),CK7(-),GPC3(70%弱+),GS(100%弱+),Hepa(+),HSP70(弱+),Ki-67(密集区30%阳性)16S01550-005：AFP(-),Arg-1(100%+),CD34(血管+),CK19(-),CK7(-),GPC3(弱+),GS(100%弱+),Hepa(+),HSP70(-)Ki-67(30%阳性)'
    text = normalize_text(text)
    a = split_structured_text(text)
    print a

if __name__ == '__main__':
    main()