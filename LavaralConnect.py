'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 
# __Version__: 
'''
'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 16.12.2021
# __Version__: 连接lavaral forge
'''
from mysql.connector import connect,cursor
from sshtunnel import SSHTunnelForwarder
import time

def LavaralConnect():
    with open('id_rsa') as f:
        private_key = f.read()

    with SSHTunnelForwarder(
            ('',22),
            ssh_username = 'forge',
            ssh_private_key_password=private_key,
            remote_bind_address=('127.0.0.1',3306)) as server:
        conn = connect(host='127.0.0.1',
            port = server.local_bind_port,
            user='forge',
            passwd = '',
            db='gewinn_spiel')
        cursor = conn.cursor()
        cursor.execute('select `id`,`receipt` from raffles where `is_email_verified`=1 and receipt_beleg is null')
        
        # desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        # data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
        data_dict = [row for row in cursor.fetchall()]
        data_dict = dict(data_dict)
        return data_dict

def LavaralUpload(result):
    with open('id_rsa') as f:
        private_key = f.read()
    with SSHTunnelForwarder(
            ('',22),
            ssh_username = 'forge',
            ssh_private_key_password=private_key,
            remote_bind_address=('127.0.0.1',3306)) as server:
        conn = connect(host='127.0.0.1',
            port = server.local_bind_port,
            user='forge',
            passwd = '',
            db='gewinn_spiel')
        cursor = conn.cursor()
        for record in result:
            cursor.execute(f"UPDATE raffles SET `receipt_beleg` = '{result[record][0]}' WHERE `id` = {record}")
            cursor.execute(f"UPDATE raffles SET `receipt_date` = '{result[record][1]}' WHERE `id` = {record}")
        conn.commit()    
if __name__ == "__main__":
    t = time.time()
    print(LavaralConnect())
    print(time.time()-t)