#encoding:utf8
import xlrd
import os
import json
import random

rawFilePath = 'pathology reports and extraction results.xls'
bk = xlrd.open_workbook(rawFilePath,on_demand=True)
table = bk.sheet_by_index(0)
nrows = table.nrows
pair_list = {'G':(2,3),'S':(8,9),'embolus':(14,15),'type':(20,21),'stage':(27,28),'location':(33,34)}
agreement_dict = {}
for key in pair_list:
    same_num = float(0)
    for i in range(1,nrows):
        if table.cell(i,pair_list[key][0]).value == table.cell(i,pair_list[key][1]).value:
            same_num += 1
    agreement = same_num/(nrows-1)
    agreement_dict[key] = agreement
print agreement_dict