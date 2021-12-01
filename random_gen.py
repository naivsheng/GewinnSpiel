'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 17.11.2021 
# __Version__: 
# 生成随机数，指向数据库中的某一图片
'''
import random
from creat_connect import create_connection
from mysql.connector import cursor

def Generate():
    '''
        通过三方生成范围内（清洗后的文件总数）的随机数
    '''
    # random.seed() # 通过第三方获取种子，生成随机数
    connection = create_connection("localhost", "root", "admin","db") # 创建链接
    if not connection:
        create_database_query = "CREATE DATABASE db" #创建database
        database_query(connection, create_database_query)
    cursor = connection.cursor()
    query = "select count(*) from uploads"
    cursor.execute(query)
    connection.commit()
    count_rd = cursor.fetchall()
    summe = count_rd[0][0]   # 获取清洗后的文件数
    num = random.randint(1,summe)
    cursor.execute(f"select email,summe,data from uploads where `id`={num}" )
    results = cursor.fetchall()
    with open('image.png','wb') as f:
        f.write(results[0][2])
    return num, results[0][0], results[0][1], 'image.png'

if __name__ == '__main__':
    print(Generate())