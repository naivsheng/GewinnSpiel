'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 10.11.2021
# __Version__: 直线检测
'''
#coding=utf-8
import cv2
import numpy as np  
from math import fabs,sin,cos,radians

def hough(img):
    # img = cv2.imread(f, 0)
    image = img
    img = cv2.GaussianBlur(img,(3,3),0) # 高斯矩阵越大越模糊
    edges = cv2.Canny(img, 50, 150, apertureSize = 3)
    lines = cv2.HoughLines(edges,1,np.pi/180,118) # 线的最小长度，这里对最后一个参数使用了经验型的值
    result = img.copy()
    for rho_avg,theta_avg in lines[0]:
        if  (theta_avg < (np.pi/4. )) or (theta_avg > (3.*np.pi/4.0)): #垂直直线
            #该直线与第一行的交点
            pt1 = (int(rho_avg/np.cos(theta_avg)),0)
            #该直线与最后一行的焦点
            pt2 = (int((rho_avg-result.shape[0]*np.sin(theta_avg))/np.cos(theta_avg)),result.shape[0])
            # 旋转方向判断
            if pt1[0] == pt2[0] or pt1[1] == pt2[1]: # 旋转90度
                img = rotate_bound(image,theta_avg + 90)
            elif (pt1[0]-pt2[0])/(pt1[1]-pt2[1]) > 0:
                # img = rotate_bound(image,90+theta_avg)
                img = rotate_bound(image,theta_avg)
            else:
                # img = rotate_bound(image,90-theta_avg)
                img = rotate_bound(image,-theta_avg)
            cv2.line(img, pt1, pt2, (255))
        else: #水平直线
            # 该直线与第一列的交点
            pt1 = (0,int(rho_avg/np.sin(theta_avg)))
            #该直线与最后一列的交点
            pt2 = (result.shape[1], int((rho_avg-result.shape[1]*np.cos(theta_avg))/np.sin(theta_avg)))
            if pt1[0] == pt2[0] or pt1[1] == pt2[1]: # 无需旋转
                img = rotate_bound(image,theta_avg)
            elif (pt1[0]-pt2[0])/(pt1[1]-pt2[1]) > 0:
                img = rotate_bound(image,theta_avg)
            else:
                img = rotate_bound(image,-theta_avg)
            cv2.line(img, pt1, pt2, (255), 1)
    print(theta_avg)
    cv2.imshow('ww',img)
    cv2.waitKey(0)
    return img
    

def rotate_bound(image,angle):
    '''
        根据获得的直线，旋转图片
        + 逆时针，- 顺时针
    '''
    h,w = image.shape[:2] # 返回（高，宽，色彩通道数），此处取前两个值返回
    newW = int(h * fabs(sin(radians(angle))) + w * fabs(cos(radians(angle))))
    newH = int(w * fabs(sin(radians(angle))) + h * fabs(cos(radians(angle))))
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    M[0,2] += (newW-w) / 2
    M[1,2] += (newH - h) / 2
    return cv2.warpAffine(image,M,(newW,newH),borderValue=(255,255,255))
