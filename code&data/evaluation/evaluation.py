#encoding:utf8
import json
import os
gold_json_path = 'gold_standard.json'
prediction_json_path = 'prediction_results.json'

def get_result_dict(element,json_path):
    result_dict = {}
    result_list = json.load(open(json_path))
    id_list = [1, 357, 72, 121, 48, 257, 13, 433, 315, 153, 201, 172, 147, 360, 419, 278, 124, 32, 431, 345, 418, 310, 328, 327, 4, 12, 272, 320, 114, 83, 485, 202, 99, 5, 271, 168, 11, 63, 318, 104, 374, 229, 49, 417, 214, 460, 296, 105, 199, 37, 428, 35, 54, 489, 359, 325, 409, 488, 264, 279, 154, 373, 432, 143, 67, 47, 8, 157, 149, 218, 125, 462, 190, 221, 343, 178, 117, 165, 22, 85, 10, 7, 486, 127, 69, 405, 371, 487, 425, 132, 195, 442, 103, 244, 313, 444, 44, 79, 20, 156, 252, 344, 151, 384, 458, 312, 163, 426, 274, 386, 142, 394, 308, 112, 126, 466, 102, 17, 145, 205, 31, 414, 247, 222, 131]

    element_list = ["tumor_type","grade","G_score","S_score","embolus","location"]
    if element == 'all':
        for e in element_list:
            for result in result_list:
                if result and result['report_id'] in map(str, id_list): 
                    key = e+'_'+result['report_id']
                    result_dict[key] = result[e]
    else:
        for result in result_list:
            if result and result['report_id'] in map(str, id_list): 
                key = element+'_'+result['report_id']
                result_dict[key] = result[element]
    return result_dict
    
def calculate_p_r_f(gold_dict,prediction_dict):
    tp = 0
    gold_num = 0
    prediction_num = 0
    print len(gold_dict),len(prediction_dict)
    if len(gold_dict) != len(prediction_dict):
        print "[ERROR] Different Length of Gold and Prediction"
        return 
    else:
        for key in prediction_dict:
            if prediction_dict[key]:
                prediction_dict[key] = set(prediction_dict[key])
            if gold_dict[key]:
                gold_dict[key] = set(gold_dict[key])
            if gold_dict[key]:
                gold_num += 1
            if prediction_dict[key]:
                prediction_num += 1
            if prediction_dict[key] and gold_dict[key] == prediction_dict[key]:
                tp += 1
        precision = float(tp)/float(prediction_num)
        recall = float(tp)/float(gold_num)
        f_score = 2*precision*recall/(precision+recall)
    return precision,recall,f_score
element_list = ["tumor_type","grade","G_score","S_score","embolus","location"]
#element_list = ["embolus"]
for element in element_list:
    gold_dict = get_result_dict(element,gold_json_path)
    prediction_dict = get_result_dict(element,prediction_json_path)
    print element
    print calculate_p_r_f(gold_dict,prediction_dict)
        
all_gold_dict = get_result_dict('all',gold_json_path)
all_prediction_dict = get_result_dict('all',prediction_json_path)
print 'all'
print calculate_p_r_f(all_gold_dict,all_prediction_dict)
