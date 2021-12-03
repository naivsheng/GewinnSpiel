'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 03.12.2021
# __Version__: get data from s3
'''
import boto3
import os
from GewinnSpiel import DataBase
import cv2
import time
'''
from boto_test import create_bucket
s3_resourse = boto3.resource('s3')
test_bucket_name, test_response = create_bucket(bucket_prefix='testout',s3_connection=s3_resourse.meta.client)
'''

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_BUCKET = 'gewinn-spiel'
AWS_DEFAULT_REGION = 'eu-central-1'
AWS_USE_PATH_STYLE_ENDPOINT = False

t=time.time()

# s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_DEFAULT_REGION)
s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_DEFAULT_REGION)
# for bucket in s3_resource.buckets.all():
#     print(bucket.name)
gewinn_spiel = s3_resource.Bucket(name = AWS_BUCKET)
'''
filepath = os.getcwd() + '\\'
filepath = filepath + 'pic\\'
os.chdir(filepath)
filelist = os.listdir(filepath)
for f in filelist:
    img = cv2.imread(f,0)
    print(DataBase(img))
    # upload
    # print(f,'uploading')
    # s3_resource.Object(AWS_BUCKET, f).upload_file(Filename=f)
print(time.time()-t)
input('check')
'''

# download
for object in gewinn_spiel.objects.all():
    f = 'tmp.' + object.key.split('.')[1]
    s3_resource.Object(AWS_BUCKET, object.key).download_file(f) # download tmp file
    img = cv2.imread(f,0)
    print(DataBase(img))

print(time.time()-t)
# input('check')
