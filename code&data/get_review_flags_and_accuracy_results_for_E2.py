#encoding:utf8
import xlrd
import os
import json
import random

	
def getReviewFlag(rawFilePath,testSize,resultCol,flagCol):
    '''Get flagNum, flaggedErrorNum and systemErrorNum for every sample size in [100,200,300,400,493]'''
    bk = xlrd.open_workbook(rawFilePath,on_demand=True)
    table = bk.sheet_by_index(0)
    nrows = table.nrows
    testList = random.sample(range(1,nrows),testSize)
    resultDict = {}
    resultDict['flagNum']=resultDict['systemErrorNum']=resultDict['errorNum']=0
    for i in testList:
        r = int(i)
        if table.cell(r,flagCol).value != '':
            resultDict['flagNum'] += 1
            if table.cell(r,resultCol).value == 'f':
                resultDict['errorNum'] += 1
        #print table.cell(r,systemCol).value
        if table.cell(r,resultCol).value == 'f':
            resultDict['systemErrorNum'] += 1
    for key in resultDict.keys():
        resultDict[key] = str(resultDict[key])
    return resultDict

    
def calculate_accuracy_up(sample_size, random_times, data_array):
    '''calculate the accuracy and review flags rate'''
    FN_sum = 0
    FEN_sum = 0
    SEN_sum = 0
    for data in data_array:
        FN_sum += float(data['flagNum'])
        FEN_sum += float(data['errorNum'])
        SEN_sum += float(data['systemErrorNum'])
    flag_rate = FN_sum/(sample_size*random_times)
    accuracy = 1 - SEN_sum/(sample_size*random_times)
    accuracy_after = 1 - (SEN_sum-FEN_sum)/(sample_size*random_times)
    accuracy_up = accuracy_after - accuracy
    return flag_rate, accuracy, accuracy_after, accuracy_up
    
	
def main():
    rawFilePath = 'pathology reports and extraction results.xls'
    flag_num_file = 'review_flags_results.csv'
    accuracy_file = 'accuracy_results.csv'
    flag_header_list = ['sample size', 'flagNum', 'flaggedErrorNum', 'systemErrorNum']
    accuracy_header_list = ['sample size', 'flag_rate', 'accuracy', 'accuracy_after', 'accuracy_up']
    testSizeList = [100,200,300,400,493]
    resultCol = 22
    flagCol = 23
    random_times = 5
    f_1 = open(flag_num_file,'w')
    f_1.write(','.join(flag_header_list)+'\n')
    f_2 = open(accuracy_file,'w')
    f_2.write(','.join(accuracy_header_list)+'\n')
    for testS in testSizeList:
        samples = []
        j = 0
        while j < random_times:
            sample = getReviewFlag(rawFilePath,testS,resultCol,flagCol)
            samples.append(sample)
            j += 1
        #get accuracy before and after correct review flags
        accuracy_results = calculate_accuracy_up(testS, random_times, samples)
        f_2.write(str(testS)+','+','.join(map(str,accuracy_results))+'\n')
        print testS, accuracy_results
        for dict in samples:
            f_1.write(str(testS)+','+','.join(dict.values())+'\n')
    f_1.close()
    f_2.close()
    #generateTandT(rawFilePath,trainFilePath,testFilePath,testSize)
if __name__ == "__main__":
    main()
    