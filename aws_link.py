'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 16.12.2021
# __Version__: get data from s3 according to the Database
'''
import boto3
import os
from GewinnSpiel import DataBase
import cv2
import time
from LavaralConnect import LavaralConnect, LavaralUpload

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_BUCKET = 'gewinn-spiel'
AWS_DEFAULT_REGION = 'eu-central-1'
AWS_USE_PATH_STYLE_ENDPOINT = False

t=time.time()

s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_DEFAULT_REGION)
gewinn_spiel = s3_resource.Bucket(name = AWS_BUCKET)
# download
# 连接db，获取仍未进行识别的记录，存储为字典 id:pic
# 遍历s3中的图片，若在dic中则下载识别，传回单据信息
# 上传结果到db
data_dict = LavaralConnect()
dict_new = dict(zip(data_dict.values(),data_dict.keys()))   # 图片名：id
result = {}
for object in gewinn_spiel.objects.all():
    if 'images/' not in object.key.split('.')[0]:
        continue
    if object.key.split('/')[1] in dict_new:
        f = 'tmp.' + object.key.split('.')[1]
        s3_resource.Object(AWS_BUCKET, object.key).download_file(f) # download tmp file
        img = cv2.imread(f,0)
        result[dict_new[object.key.split('/')[1]]] = DataBase(img)
        with open('result.txt','a+') as result_file: # 数据备份到文件，防止server崩溃
            result_file.write(dict_new[object.key.split('/')[1]],result[dict_new[object.key.split('/')[1]]] )
LavaralUpload(result)

print(time.time()-t)
