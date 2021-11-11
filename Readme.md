<!--
 * @# -*- coding: UTF-8 -*-
 * @# __Author__: Yingyu Wang
 * @# __date__: 
 * @# __Version__: 
-->
<!--
 * @# -*- coding: UTF-8 -*-
 * @# __Author__: Yingyu Wang
 * @# __date__: 
 * @# __Version__: 
-->
<!--
 * @# -*- coding: UTF-8 -*-
 * @# __Author__: Yingyu Wang
 * @# __date__: 2021-11-04
 * @# __Version__: 
-->
# 实现图片数据识别
## 数据拉取
从云端拉取数据到本地以进行后续操作
## 图片预处理
直线识别（高斯模糊消除噪点，hough变换，旋转图片）
提高图片亮度、灰度处理、提高对比度
## 图像识别
调用tesseract库进行ocr识别
## 数据处理
从得到的数据中查找Rechnungnr
若没有账单信息，旋转图片重复2-4。仍无识别结果则对图片进行标记
若得到账单信息，将数据记录归档。在账单库查找该账单信息，判断账单信息是否正确。若数据不正确则对图片那进行标记
提取标记的图片，进行人工核查

# log

## 11.11.2021
优化算法流程
TODO 前期指定拍照位置、线下or线上

流程
contrast
尝试提高亮度
读取单号、日期
对没有数据的图片旋转
尝试提高亮度
读取单号、日期

对日期数据进行清洗

## 10.11.2021
测试外省他人上传的图片
确定图片所需的格式（拍照范围）
在调整亮度前增加判定，若未能读取出任何信息则旋转图片90°
调整亮度、对比度进行ocr过程
若无结果，则旋转图片180°，重新识别

## 05.11.2021
1.图像增强对比度contrast后未能提高识别范围
2.仅通过边缘检测，会损失大量细节，识别范围增加，但准确度低
3.尝试方案
->尝试提高亮度+增强对比度，再进行边缘、直线检测、旋转，将检测后的图像进行识别
->尝试边缘、直线检测后将原图进行旋转，提高旋转后的原图亮度、对比度，进行识别
->尝试模糊，反相，亮度，对比度
4.解决方案
提高亮度，旋转，识别：有效但系数原因效果一般
5.设计算法：自动提高图片亮度
通过直方图等计算图片的平均亮度
根据初始化最大亮度，对图像进行修改

## 04.11.2021
搭建霍夫变换
通过直线检测旋转图片
测试边缘检测获得图像的识别结果：损失细节
## 03.11.2021
提高对比度 测试识别结果：效果甚微
提高亮度 测试识别结果：有一定效果
