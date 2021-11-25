'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 
# __Version__: 创建MySQL连接
'''
import mysql.connector  # pip install mysql-connector-python
from mysql.connector import Error

def create_connection(host_name, user_name, user_password):
    connection = None
    try:
  #创建连接
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("连接成功")
    except Error as e:
        print(f"错误 '{e}' 发生")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
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

if __name__ == '__main__':
    connection = create_connection("localhost", "root", "") # 创建链接
    create_database_query = "CREATE DATABASE new" #创建database
    create_database(connection, create_database_query)