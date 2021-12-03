'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 25.11.2021
# __Version__: 文件读取更改为从数据库拉取数据
# 账单信息识别测试
预处理中的取消旋转判定
由于Beleg.Nr不唯一：获取datum信息以定位信息
对未能识别的图片顺时针旋转180°
# 仍未能识别：hough+contrast+rotate
测试结果：不能读取gif格式
    直线检测hough变换，文本定位√
    旋转矫正rotate√
    提高亮度，提高对比度√
    # 图像匹配 文字区域检测 序列切分识别
    文字提取ocr
'''

from PIL import Image, ImageStat
import pytesseract
import argparse
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from hough import hough
import re
import time
from predata import DatumCleaning, BelegCleaning

def rotate(img):
    '''
        旋转矫正：预处理后没有识别结果，将图片旋转180再次识别
    '''
    return np.rot90(img,k=2) # 逆时针旋转90，k表示旋转次数，-1表示顺时针

def contrast(img):
    '''
        均衡化: 增强对比度，提高识别准确率，但提升有限
    '''
    '''
    # 彩色
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    plane = []
    planes = cv2.split(img) # 将图片分为三个单通道
    for i in range(len(planes)):
        plane.append(clahe.apply(planes[i]))
    cl1 = cv2.merge(plane)
    return cl1
    '''
    # 灰度图
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    cl1 = clahe.apply(img)
    return cl1
    
def ocr(image):
    '''
        识别
    '''
    string = pytesseract.image_to_string(image)
    return string

def imgBrightness(img,c,b):
    '''
        提高亮度,提高识别准确率
    '''
    # rows,cols,channels = img.shape
    rows, cols = img.shape # 灰度图
    # blank = np.zeros([rows,cols,channels],img.dtype)
    blank = np.zeros([rows,cols],img.dtype)
    rst = cv2.addWeighted(img,c,blank,1-c,b)
    return rst

def bright(f):
    '''
        计算图片亮度
    '''
    img = Image.open(f).convert('L')
    stat = ImageStat.Stat(img)
    return stat.rms[0]

def findresult(img):
    '''
        通过提高亮度增加清晰度
    '''
    result = ocr(img)
    # pattern_filiale_nr = re.compile(r'\D\s\d{9}\s')   # 单号9位数字 非数字+空+数字9位+空 规避fax
    # pattern_filiale_nr = re.compile(r'[\S\s][\s]\d{9}[\s]')    # 尝试获取所有数据，后续再进行清洗
    pattern_filiale_nr = re.compile(r'\D{2}\d{9}\D') 
    pattern_webshop_nr = re.compile(r'\s1\d{7}\s') # 网店单号更新为以1开头的8位
    pattern_datum = re.compile(r'\d{2}[.]\d{2}[.]\d{4}')
    findout_beleg = pattern_filiale_nr.findall(result)
    findout_datum = pattern_datum.findall(result)
    for counter in range(5):
        if not findout_datum:
            findout_datum = pattern_datum.findall(result)
        if not findout_beleg:
            findout_beleg = pattern_webshop_nr.findall(result)
        else:
            if findout_datum:
                break
        result = ocr(imgBrightness(img,1.1 + (counter / 10) * 2,3))
    '''
    check_file = filepath + f.split('.')[0] + '.txt'
    with open(check_file, "a", encoding="utf-8") as f2:
        f2.write(result) # 写入'''
    return findout_beleg,findout_datum
    
def main_neu(img):
    result = ocr(img)
    pattern_filiale_nr = re.compile(r'\D\W\d{9}\s') 
    pattern_webshop_nr = re.compile(r'\s1\d{7}\s') # 网店单号更新为以1开头的8位
    pattern_datum = re.compile(r'\d{2}[.]\d{2}[.]\d{4}')
    findout_datum = []
    findout_beleg = []
    for counter in range(5):
        findout_beleg = pattern_filiale_nr.findall(result) if not findout_beleg else findout_beleg
        findout_datum = pattern_datum.findall(result) if not findout_datum else findout_datum
        if not findout_datum and not findout_beleg:
            pass
        elif findout_datum and findout_beleg:
            findout_datum = DatumCleaning(findout_datum)
            findout_beleg = BelegCleaning(findout_beleg)
        elif findout_datum:
            findout_datum = DatumCleaning(findout_datum)
            findout_beleg = pattern_webshop_nr.findall(result)
            if findout_beleg:
                findout_beleg = BelegCleaning(findout_beleg)
        else:
            findout_beleg = BelegCleaning(findout_beleg)
        if findout_datum and findout_beleg:
            break
        result = ocr(imgBrightness(img,1.1 + (counter / 10), 3))    
    return findout_beleg,findout_datum

def run():
    '''
        本地拉取
    '''
    t = time.time()
    filepath = os.getcwd() + '\\pic\\'
    os.chdir(filepath)
    filelist = os.listdir(filepath)
    for f in filelist:
        if ('.jpg' in f) or ('.bmp' in f) or ('.png' in f):
            print('actuelle file:',f)
            img = cv2.imread(f,0) # 灰度
            # img = cv2.imread(f)
            img = contrast(img)
            findout_beleg,findout_datum = main_neu(img)
            if not findout_datum and not findout_beleg:
                print('rotate')
                img = rotate(img)
                findout_beleg,findout_datum = main_neu(img)
            if not findout_datum and not findout_beleg:
                print('does not find out a result')
            else:
                print(findout_beleg,findout_datum)    
    print('用时：',time.time()-t)

def DataBase(img):
    '''
        数据库拉取
    '''
    # t = time.time()
    img = contrast(img)
    findout_beleg,findout_datum = main_neu(img)
    if not findout_datum and not findout_beleg:
        # print('rotate')
        img = rotate(img)
        findout_beleg,findout_datum = main_neu(img)
    findout_beleg = '-' if not findout_beleg else findout_beleg
    findout_datum = '-' if not findout_datum else findout_datum
    return findout_beleg,findout_datum 
    # print('用时：',time.time()-t)

if __name__ == "__main__":
    run()
