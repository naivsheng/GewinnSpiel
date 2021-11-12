'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 11.11.2021
# __Version__: 读取得数据进行清洗、归档
'''
import re

def DatumCleaning(data_list):
    '''
        确认0<月份<13，否则替换月份中的4->1；
        确认0<日期<32，否则替换日期中的4->1
        若有多个数据，直接删除不符合规范的数据
        去重
    '''
    # print(data_list)
    result = ''
    for data in data_list:
        result = ''
        if data.split('.')[-1] != '2021':
            continue
        else: 
            result = data.split('.')[-1]
        if int(data.split('.')[1]) > 12: 
            continue
        else:
            result = data.split('.')[1] + '.' + result
        if int(data.split('.')[0]) > 31: 
            continue
        else:
            result = data.split('.')[0] + '.' + result
        break
    if len(result) == 10:
        return result
    else:
        result == ''
        try:
            pre = data_list.split('.')
        except:
            pre = data_list[0].split('.')
        y = pre[2].replace('4','1')
        if y != '2021': return ''
        m = pre[1]
        if int(m)>12: m = m.replace('4','1')
        if int(m)>12:return ''
        d = pre[0]
        if int(d)>31: m = m.replace('4','1')
        if int(d)>31:return ''
        result = d + '.' + m + '.' + y
    return result

def BelegCleaning(datalist):
    '''
        清洗beleg数据
        删除多余字符
        将错读的字符串首字更改为 '1'
    '''
    data = {'4':'1','6':'5'}    # 没有由 6或4 为首字的单号
    data_rest = ['1','2','5','7']
    '''pre = ''
    if len(datalist)>1:
        for beleg in datalist:
            if beleg[0].isdigit():
                pass
            else:
                pre = re.sub('[^\d]','',pre)
    if not pre:
        # pre = datalist[-1].split(' ')[1]
        # pre = re.sub('[^\d]','',pre)
        if len(datalist[-1]) == 9:
            pre = datalist[-1][2:-1]
        else: pre = datalist[-1][]
    if pre[0] in data:
        result = data[pre[0]] + pre[1:]
    else: result = pre
    return result
    '''
    # 更新逻辑
    result = []
    for beleg in datalist:
        if len(beleg) == 12:    # offline
            # pre = re.sub('^[0-9]','',beleg)
            pre = beleg[2:-1]
            if pre[0] in data:
                result.append(data[pre[0]] + pre[1:])
            elif pre[0] not in data_rest:
                pass
            else: result.append(pre)
        else:
            # result.append(re.sub('[^0-9]','',beleg))
            result.append(beleg[1:-1])
    if len(result) > 0: 
        return result[0]
    else: return ''
    