import cv2
import numpy as np
import matplotlib.pyplot as plt

 
#1.先水平分割，再垂直分割
# 对图片进行垂直分割
def verticalCut(img):
    (x,y)=img.shape #返回的分别是矩阵的行数和列数，x是行数，y是列数
    # if y ==1:
    #     return
    pointCount=np.zeros(y,dtype=np.uint8)#每列白色的个数
    
    #i是列数，j是行数
    
    for i in range(0,y):
        for j in range(0,x):
            # if j<15:
            if(img[j,i]==255):
                pointCount[i]=pointCount[i]+1

    return pointCount

 
#对图片进行水平分割,返回的事照片数组
def horizontalCut(img):
    x,y=img.shape #返回的分别是矩阵的行数和列数，x是行数，y是列数
    
    # if y ==1:
    #     return
    pointCount=np.zeros(x,dtype=np.uint8)#每行白色的个数
    
    
    for i in range(0,x):
        for j in range(0,y):
            if(img[i,j]==255):
                pointCount[i]=pointCount[i]+1
    
    
    
    return pointCount

    
    
    
import os

def imgThreshold(img):
    rosource,binary=cv2.threshold(img,121,255,cv2.THRESH_BINARY)
    return binary

def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    # if x == zero_list or y == zero_list:
    #     return float(1) if x == y else float(0)

    # method 1
    # res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    # cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    # method 2
    # cos = bit_product_sum(x, y) / (np.sqrt(bit_product_sum(x, x)) * np.sqrt(bit_product_sum(y, y)))

    # method 3
    dot_product, square_sum_x, square_sum_y = 0, 0, 0
    for i in range(len(x)):
        dot_product += x[i] * y[i]
        square_sum_x += x[i] * x[i]
        square_sum_y += y[i] * y[i]
    cos = dot_product / (np.sqrt(square_sum_x) * np.sqrt(square_sum_y))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内




directory_name = ("1-10")
input_pic = cv2.imread("/home/zhaoyx/screen_detector/crop_number/3.jpg_2.jpg")
input_pic = cv2.cvtColor(input_pic,cv2.COLOR_BGR2GRAY)
binary=imgThreshold(input_pic)
x,y=binary.shape
binary = np.pad(binary, ((0, 0),(0, 8-y)), mode="constant")

point_y = horizontalCut(binary )
point_x = verticalCut(binary)
point_input = np.hstack((point_y, point_x))
c_input = np.vstack((point_x,point_y)).T
for fileName in os.listdir(directory_name):
    #先读取图片
    img = cv2.imread(directory_name + '/' +fileName)
    

    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    binary=imgThreshold(img)
    x,y=binary.shape
    
    if y<8:
        
        binary = np.pad(binary, ((0, 0),(0, 8-y)), mode="constant")
    
    print(fileName)
    point_y = horizontalCut(binary)
    point_x = verticalCut(binary)
    
    c = np.vstack((point_x,point_y)).T
    

    point = np.hstack((point_y, point_x))
    
    if len(point) == len(point_input):
        # x = cosine_similarity(point, point_input)
        x = cosine_similarity(c,c_input)
        print(x)

