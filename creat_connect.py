'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 
# __Version__: 创建MySQL连接
'''
# import mysql.connector  # pip install mysql-connector
from mysql.connector import Error,connect,cursor
import os
import GewinnSpiel as GS
import numpy as np
import cv2

def create_connection(host_name, user_name, user_password,db):
    connection = None
    try:
  #创建连接
        connection = connect(
            host=host_name,
            user=user_name,
            passwd=user_password
            ,auth_plugin = "mysql_native_password",
            database = db,
            buffered = True
        )
        print("连接成功")
        return connection
    except Error as e:
        print(f"错误 '{e}' 发生")
        return None


def database_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def select_by_database(connection):
    cmd = connection.cursor()
    cmd.execute("select id, name, age from stu")
    # 使用fetchone()返回一条结果集，每调用一次之后，内部指针会指向下一条结果集
    print(cmd.fetchone()) 
    print(cmd.fetchone()) 
    # 可以使用fetchall()，获取所有的查询结果集，返回值为一个tuple，每一个元素是一个list
    print(cmd.fetchall()) 

    # 执行原生SQL语句 插入一条数据
    cmd.execute("insert into stu (id, name, age) values (4, 'LiBai', 99)")
    # 预处理格式
    cmd.execute("select * from stu where id=%s and name=%s", (1, 'LiMing'))

def pic2sql():
    connection = create_connection("localhost", "root", "admin","db") # 创建链接
    if not connection:
        create_database_query = "CREATE DATABASE db" #创建database
        database_query(connection, create_database_query)
    cursor = connection.cursor()
    create_table_query = "CREATE TABLE IF NOT EXISTS `uploads` (`id` INT AUTO_INCREMENT PRIMARY KEY,`email` VARCHAR(50),\
        `summe` VARCHAR(7),`data` mediumblob null,`datum_result` VARCHAR(10),`nummer_result` VARCHAR(10),`verify_code` VARCHAR(100))"
    database_query(connection,create_table_query)
    sql = "INSERT INTO uploads (`email`, `data`) VALUES (%s, %s)"
    filepath = os.getcwd() + '\\pic\\'
    os.chdir(filepath)
    filelist = os.listdir(filepath)
    
    # 将图片写入DB
    for files in filelist:
        print(files)
        row = cursor.lastrowid
        with open(files,'rb') as f:
            val = ("example@123.com", f.read())
        cursor.execute(sql,val)
        connection.commit() # 数据表内容有更新，必须使用到该语句
        if row != cursor.lastrowid:
            print(cursor.lastrowid, "记录插入成功。")
        else: print('记录插入失败')
    
def result2DB():
    connection = create_connection("localhost", "root", "admin","db") # 创建链接
    if not connection:
        create_database_query = "CREATE DATABASE db" #创建database
        database_query(connection, create_database_query)
    cursor = connection.cursor()
    cursor.execute('select * from uploads where datum_result is NULL')  # 跳过以处理过的数据
    results = cursor.fetchall()
    for row in results:
        id_ = row[0]
        email = row[1]
        img = row[3]
        with open('image.png','wb') as f:
            f.write(img)
        img = cv2.imread('image.png',0)
        findout_beleg,findout_datum = GS.DataBase(img)
        update_query = f"UPDATE uploads SET nummer_result = '{findout_beleg}' WHERE `id` = {id_}"
        database_query(connection, update_query)
        update_query = f"UPDATE uploads SET datum_result = '{findout_datum}' WHERE `id` = {id_}"
        database_query(connection, update_query)
        os.remove('image.png')
        connection.commit()

def delete_repeat():
    '''
        抽奖前进行去重，从tmp表中进行抽奖
    '''
    connection = create_connection("localhost", "root", "admin","db") # 创建链接
    cursor = connection.cursor()
    query = "CREATE TABLE tmp SELECT * FROM uploads GROUP BY (nummer_result);"
    database_query(connection,query)
    query = "DELETE FROM tmp WHERE `nummer_result` ='-';"   # 去空
    database_query(connection,query)
    '''  # 替换原表
        DROP TABLE person_tbl;
        ALTER TABLE tmp RENAME TO person_tbl;
    '''
def reset_id():
    connection = create_connection("localhost", "root", "admin","db") # 创建链接
    cursor = connection.cursor()
    query = "ALTER TABLE `tmp` DROP COLUMN `id`; "
    database_query(connection,query)
    query = "    ALTER TABLE `tmp` ADD `id` int(7) unsigned NOT NULL AUTO_INCREMENT FIRST,\
            ADD PRIMARY KEY (`id`),AUTO_INCREMENT = 0 ROW_FORMAT = COMPACT;"
    database_query(connection,query)
if __name__ == '__main__':
    # result2DB()
    delete_repeat()