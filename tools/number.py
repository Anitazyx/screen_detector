#https://blog.csdn.net/weixin_43988887/article/details/90214840

import cv2
import numpy as np
import matplotlib.pyplot as plt
 
#图像二值化处理
def imgThreshold(img):
    rosource,binary=cv2.threshold(img,121,255,cv2.THRESH_BINARY)
    return binary
 
#1.先水平分割，再垂直分割
# 对图片进行垂直分割
def verticalCut(img, fileName):
    (x,y)=img.shape #返回的分别是矩阵的行数和列数，x是行数，y是列数
    pointCount=np.zeros(y,dtype=np.float32)#每列白色的个数
    # x_axes=np.arange(0,y)
    #i是列数，j是行数
    tempimg=img.copy()
    for i in range(0,y):
        for j in range(0,x):
            # if j<15:
            if(tempimg[j,i]==255):
                pointCount[i]=pointCount[i]+1
    # figure=plt.figure(str(img_num))
    # for num in range(pointCount.size):
    #     pointCount[num]=pointCount[num]
    #     if(pointCount[num]<0):
    #         pointCount[num]=0
    # plt.plot(x_axes,pointCount)
    start = []
    end = []
    # 对照片进行分割
    print(pointCount)
    for index in range(1, y-1):
        # 上个为0当前不为0，即为开始
        if ((pointCount[index-1] == 0) & (pointCount[index] != 0)):
            start.append(index)
        # 上个不为0当前为0，即为结束
        elif ((pointCount[index] == 0) & (pointCount[index -1] != 0)):
            end.append(index)
    print(start, end)
    imgArr=[]
    for idx in range(0,len(start)):
        
        tempimg=img[ :,start[idx]:end[idx]]
        cv2.imwrite("crop_number/"+fileName+"_"+str(idx)+".jpg", tempimg)
        imgArr.append(tempimg)

    return imgArr

 
#对图片进行水平分割,返回的事照片数组
def horizontalCut(img, fileName):
    (x,y)=img.shape #返回的分别是矩阵的行数和列数，x是行数，y是列数
    print(x, y)
    pointCount=np.zeros(x,dtype=np.uint8)#每行白色的个数
    # x_axes=np.arange(0,y)
    for i in range(0,x):
        for j in range(0,y):
            if(img[i,j]==255):
                pointCount[i]=pointCount[i]+1
    # plt.plot(x_axes,pointCount)
    start=[]
    end=[]
    #对照片进行分割
    print(pointCount)

    for index in range(1,x):
        #上个为0当前不为0，即为开始
        if((pointCount[index]!=0)&(pointCount[index-1]==0)):
            start.append(index)
        #上个不为0当前为0，即为结束
        elif((pointCount[index]==0)&(pointCount[index-1]!=0)):
             end.append(index)
    
    crop_h = img[start[0]:end[0], :]
    cv2.imwrite("crop_h.jpg", crop_h)
    imgArr = verticalCut(crop_h, fileName)
    print(len(imgArr))
    
    
    return imgArr
 
#输入的分别是原图模板和标签
def matchTemplate(src,matchSrc,label):
    binaryc=imgThreshold(src)
    # enum { TM_SQDIFF=0, TM_SQDIFF_NORMED=1, TM_CCORR=2, TM_CCORR_NORMED=3, TM_CCOEFF=4, TM_CCOEFF_NORMED=5 }
    result=cv2.matchTemplate(binaryc,matchSrc,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    tw,th=matchSrc.shape[:2]
    tl=(max_loc[0]+th+2,max_loc[1]+tw+2)
    cv2.rectangle(src,max_loc,tl,[255,0,0])
    # cv2.putText(src,label,max_loc,fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=0.6,
    #             color=(240,230,0))
    # cv2.imshow('001',src)
    return src
    # cv2.imwrite("001.jpg", src)


import pytesseract as tess

def recognize_text(img):
    gray = cv2.cvtColor(img, 0)

    # cv2.imshow("binimg", gray)
    ret, binnary = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)
    # cv2.imshow("binmg", binnary)
    kerhel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bin1 = cv2.morphologyEx(binnary, cv2.MORPH_OPEN, kerhel1, iterations=1)
    kerhel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    bin2 = cv2.morphologyEx(binnary, cv2.MORPH_OPEN, kerhel2, iterations=1)
    # cv2.imshow("binary_img",bin2)
    text = tess.image_to_string(bin2)
    print("识别结果：", text)



path = ("data_dir/number")
import os
import torch
from torch import nn
from torch.nn import functional as F


if os.path.isdir(path):
    files = os.listdir(path)
else:
    files = [path]

for fileName in files:
    #先读取图片
   
    img = cv2.imread(path + '/' +fileName)
    print(fileName)
    # img = torch.from_numpy(img)
    # print(img.shape)

    # img = img.unsqueeze(0)
    # img = F.interpolate(img, size=(300, 150), scale_factor=None, mode='nearest', align_corners=None)

    
    # # img = img.squeeze()
    # img = img.numpy()
    

    
    # cv2.imwrite(fileName, img)
    
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    binary=imgThreshold(img)
    cv2.imwrite("b.jpg", binary)
    
    horizontalCut(binary, fileName)
    
    
    #匹配算法
    # match=cv2.cvtColor(match,cv2.COLOR_BGR2GRAY)
    # binary =imgThreshold(match)
    # src = matchTemplate(img,match,'7')
    # cv2.imwrite("output/"+os.path.basename(fileName)+".jpg", src)


    
    # recognize_text(match)



 