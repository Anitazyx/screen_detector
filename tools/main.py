#https://blog.csdn.net/gaoyu1253401563/article/details/85253511


"""
思路：根据颜色进行报警，需要解决不同位置确定风速还是雪量or雨量，还要建立一个大数组判断是那个公里标
     根据颜色与数字结合，首先要根据颜色crop出数字的位置，然后对数据进行水平&垂直方向的分割，然后匹配是那个数字
     直接根据数字进行报警，输入整张图，输出数字
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

frame = cv2.imread("crop.jpg")
# frame = frame[168:356, 430:1693]
# frame = frame[170:360, 420:1700]

# cv2.imwrite("crop.jpg", frame)
orange = np.uint8([[[144, 49, 9]]])
hsv_orange = cv2.cvtColor(orange, cv2.COLOR_BGR2HSV)
print(hsv_orange)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


# 在HSV空间中定义蓝色
# lower_blue = np.array([110, 100,100])
# upper_blue = np.array([130, 255, 255])
# lower_blue = np.array([110, 100,100])
# upper_blue = np.array([113, 255, 255])
lower_blue = np.array([115, 100,100])
upper_blue = np.array([130, 255, 255])
# 在HSV空间中定义绿色
lower_green = np.array([50, 100, 100])
upper_green = np.array([70, 255, 255])
# 在HSV空间中定义红色
lower_red = np.array([0, 120, 120])
upper_red = np.array([5, 255, 255])
# 在HSV空间中定义橙色
lower_orange = np.array([15, 100, 100])
upper_orange = np.array([25, 255, 255])
# 在HSV空间中定义黄色
lower_yellow = np.array([25, 100, 100])
upper_yellow = np.array([35, 255, 255])
# 在HSV空间中定义白色
lower_white = np.array([0, 0, 100])
upper_white = np.array([0, 0, 255])


#部分3：
# 从HSV图像中截取出蓝色、绿色、红色，即获得相应的掩膜
# cv2.inRange()函数是设置阈值去除背景部分，得到想要的区域
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
# print(blue_mask)
# print("是否为全零数组：")
# print(not(np.any(blue_mask)))
# print(type(blue_mask))
green_mask = cv2.inRange(hsv, lower_green, upper_green)

red_mask = cv2.inRange(hsv, lower_red, upper_red)
orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)


yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

white_mask = cv2.inRange(hsv, lower_white, upper_white)
# a = np.where(yellow_mask>0)
# print(a[0])
# print(min(a[1]))

# b = np.where(a[0]<90) #返回在横线之上的像素值的y的坐标的坐标
# print(b)

# c = a[1]#x值

# c = c[0:len(b[0])]#选取相应的x的坐标,有很多，但是有重复的
# x_c = c
# print(c)

# c, count= np.unique(c, return_index=True)#给他去除重复的
# print(c)
# print(count)
# x0 = c[:-1]

# x1 = c[1:]

# x = np.array(x1)-np.array(x0)#去除重复的后，要给他分段，判断不同的柱子
# x = np.where(x>1)
# print(len(x))

# h = c[x[0]+1]
# print("h", h)
# tag = count[x[0]+1]

# print(x_c[tag])
# ve = np.where(a[1]==x_c[tag])
# print(ve)
# print(len(ve[0]))





blue_res = cv2.bitwise_and(frame, frame, mask = blue_mask)
green_res = cv2.bitwise_and(frame, frame, mask = green_mask)
red_res = cv2.bitwise_and(frame, frame, mask = red_mask)
orange_res = cv2.bitwise_and(frame, frame, mask = orange_mask)
yellow_res = cv2.bitwise_and(frame, frame, mask = yellow_mask)
white_res = cv2.bitwise_and(frame, frame, mask = white_mask)



cv2.imwrite("mask_pic/red_mask.jpg", red_mask)
cv2.imwrite("res_pic/red_res.jpg", red_res)
cv2.imwrite("mask_pic/blue_mask.jpg", blue_mask)
cv2.imwrite("res_pic/blue_res.jpg", blue_res)
cv2.imwrite("mask_pic/green_mask.jpg", green_mask)
cv2.imwrite("res_pic/green_res.jpg", green_res)
cv2.imwrite("mask_pic/orange_mask.jpg", orange_mask)
cv2.imwrite("res_pic/orange_res.jpg", orange_res)
cv2.imwrite("mask_pic/yellow_mask.jpg", yellow_mask)
cv2.imwrite("res_pic/yellow_res.jpg", yellow_res)
cv2.imwrite("mask_pic/white_mask.jpg", white_mask)
cv2.imwrite("res_pic/white_res.jpg", white_res)




