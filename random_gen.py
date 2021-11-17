
'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 17.11.2021 
# __Version__: 
# 生成随机数，指向数据库中的某一图片
'''
import random

def Generate():
    '''
        通过三方生成范围内（清洗后的文件总数）的随机数
    '''
    # random.seed() # 通过第三方获取种子，生成随机数
    
    summe = 100 # 获取清洗后的文件数
    num = random.randint(1,summe)
    return num

if __name__ == '__main__':
    print(Generate())