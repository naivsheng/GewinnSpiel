'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 11.11.2021
# __Version__: 读取得数据进行清洗、归档
'''

def DataCleaning(data_list):
    '''
        确认0<月份<13，否则替换月份中的4->1；
        确认0<日期<32，否则替换日期中的4->1
        若有多个数据，直接删除不符合规范的数据
        去重
    '''
    result = []
    if len(data_list)>1:
        for data in data_list:
            pre = data.split('.')
            if int(pre[2]) != 2021:
                continue
            if int(pre[0]) > 31:
                pre[0] = pre[0].replace('4','1')
            if int(pre[1]) > 12:
                pre[1] = pre[1].replace('4','1')
            result.append(pre[0]+'.'+pre[1]+'.'+pre[2])
        result = list(set(result))  # 去重
    else:
        pre = data_list[0].split('.')
        if int(pre[2]) != 2021:
            pre[2] = pre[2].replace('4','1')
        if int(pre[0]) > 31:
            pre[0] = pre[0].replace('4','1')
        if int(pre[1]) > 12:
            pre[1] = pre[1].replace('4','1')
        result.append(pre[0]+'.'+pre[1]+'.'+pre[2])
    return result[0]