'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 29.10.2021
# __Version__: 账单信息识别测试
测试结果：不能读取gif格式
TODO 
    直线检测hough变换，文本定位√
    旋转矫正rotate√
    提高亮度，提高对比度√
    # 图像匹配 文字区域检测 序列切分识别
    文字提取ocr
'''
# import the necessary packages
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

def rotate(img):
    '''
        旋转矫正：预处理后没有识别结果，将图片旋转180再次识别
    '''
    img90 = np.rot180(img)


def plot(grayHist):
    '''
        计算灰度分布直方图
    '''
    plt.plot(range(256), grayHist, 'r', linewidth=1.5, c='red')
    y_maxValue = np.max(grayHist)
    plt.axis([0, 255, 0, y_maxValue]) # x和y的范围
    plt.xlabel("gray Level")
    plt.ylabel("Number Of Pixels")
    plt.show()

def gray(f):
    '''
        处理图片: 灰度
    '''
    img = cv2.imread(f)
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    output = f.split('.')
    outname = output[0] + '_gray.' + output[1]
    cv2.imwrite(outname,img_gray)
    '''
        # 图像的灰度级范围是0~255
        grayHist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
        plot(grayHist)  # 直方图
    '''
    dst = 255-img_gray # 反相
    ocr(dst)
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    # contrast(outname)
    # ocr(outname)
    # os.remove(os.getcwd() + '\\' + outname) # remove the cache

def contrast(img):
    '''
        均衡化: 增强对比度，提高识别准确率，但提升有限
    '''
    # img = cv2.imread(f,0)   # -1 原图；0 灰度；1 RGB
    # grayHist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # plot(grayHist)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # cl1 = clahe.apply(img) # 灰度仅需要单相处理
    plane = []
    planes = cv2.split(img) # 将图片分为三个单通道
    for i in range(len(planes)):
        plane.append(clahe.apply(planes[i]))
    cl1 = cv2.merge(plane)
    
    # res = np.hstack((img,cl1)) # 图片合并
    return cl1
    output = f.split('.')
    out = output[0] + '_contrast.' + output[1]
    cv2.imwrite(out,cl1)
    
    # ocr(out)
    
def ocr(image):
    '''
        识别
    '''
    # image = Image.open(f)
    string = pytesseract.image_to_string(image)
    return string

def imgBrightness(img,c,b):
    '''
        提高亮度,提高识别准确率
    '''
    '''img = cv2.imread(f)
    rows, cols, channels = img.shape
    blank = np.zeros([rows,cols,channels],img.dtype)
    rst = cv2.addWeighted(img,c,blank,1-c,b) # 通过图像融合提高亮度
    # output = f.split('.')
    # out = output[0] + '_bright.' + output[1]
    # cv2.imwrite(out,rst)
    # ocr(out)'''
    rows,cols,channels = img.shape
    blank = np.zeros([rows,cols,channels],img.dtype)
    rst = cv2.addWeighted(img,c,blank,1-c,b)
    return rst

def bright(f):
    '''
        计算图片亮度
    '''
    img = Image.open(f).convert('L')
    stat = ImageStat.Stat(img)
    return stat.rms[0]

if __name__ == "__main__":
    t = time.time()
    filepath = os.getcwd()
    os.chdir(filepath)
    filelist = os.listdir(filepath)
    pattern_filiale_nr = re.compile(r'\s\d{9}\s')
    pattern_webshop_nr = re.compile(r'\s9\d{6}\s') # 网店单号更新为以1开头的8位
    for f in filelist:
        if 'test' in f:
            # stat = bright(f)
            # print(f,stat)
            # continue
            img = cv2.imread(f)
            img = hough(img) 
            # img = contrast(img)
            result = ocr(img)
            for counter in range(7):
                result = re.sub('\d\s\d{9}','',result)
                findout = pattern_filiale_nr.findall(result)
                if not findout:
                    findout = pattern_webshop_nr.findall(result)
                else:
                    print(f,counter, "fl", findout)
                    break
                if findout:
                    print(f,counter, "online", findout)
                    break
                img = imgBrightness(img,1.1 + counter / 10,3)
                result = ocr(img)
            if not findout:
                print(f,'does not find out a result')    
            # imgBrightness(f,1.5,3)
            continue
            # gray(f)
            # img = cv2.imread(f)
            # img = contrast(img)
            # mean_rgb(f)
    print('用时：',time.time()-t)
