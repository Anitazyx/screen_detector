
import cv2
import numpy as np
# import cupy as cp
import os
import argparse
from time import perf_counter
import time
from line_profiler import LineProfiler
from functools import wraps
 

#查询接口中每行代码执行的时间
def func_line_time(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        func_return = f(*args, **kwargs)
        lp = LineProfiler()
        lp_wrap = lp(f)
        lp_wrap(*args, **kwargs) 
        lp.print_stats() 
        return func_return 
    return decorator 
 

def contours_detect(mask, value, rectangle_info, color):
    h = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = h[0]
    
    for i in range(0,len(contours)): 
        
        x, y, w, h = cv2.boundingRect(contours[i])     
        
        if h>value:#有效轮廓    
               
            x_c = [x[0][0] for x in contours[i]]#轮廓的x坐标
            y_c = [x[0][1] for x in contours[i]]#轮廓的y坐标
            a_max = np.where(y_c==max(y_c))#求y最大的，也就是最下面轮廓的y的坐标的坐标
            a_max = a_max[0]
            

            
            for j in range(0, len(a_max)-1, 2):#默认轮廓绘画方式导致最下面一排的x为自小到大
                #求当前x下有几个y
                y_m = np.where([x[0][0] for x in contours[i]]==x_c[a_max[j]])
                y_c = np.array(y_c)
                b = y_c[y_m[0]]#y对应的坐标
                h = max(b)-min(b)#最大减最小为高度
            
                rectangle_info.append([x_c[a_max[j]], h, color, 1])           
            print(y_m)


        
def mask_detect_new_cp(mask, value, rectangle_info, color):
    mask_site = cp.where(mask>0)#异常颜色像素点的坐标集合

    site_x = mask_site[1]#异常像素点的x坐标
    site_y = mask_site[0]#异常像素点的y坐标，和x是一一对应，并且排序按照y从小到大排
    
    
    
    a = site_y[len(site_y)-1]
    
    a_max = cp.where(site_y==a)#求y最大的，也就是最下面轮廓的y
    a_max = a_max[0]
    
    x = site_x[a_max[0]:a_max[len(a_max)-1]]#异常像素点最下面的所有x坐标
    x0 = x[:-1]
    x1 = x[1:]
    sub_x = cp.array(x1)-cp.array(x0)#做差判断连续性
    sub_x_site = cp.where(sub_x>1)
    sub_x_site = sub_x_site[0].tolist()
    sub_x_site.append(-1)
    sub_x_site = [i + 1 for i in sub_x_site]
    tag = x[sub_x_site]
    
    for i in range(len(tag)):
        y = cp.where(site_x==tag[i])       
        y = y[0]       
        h = len(y)
        
        rectangle_info.append([tag[i], h, color, value])
    return rectangle_info



def mask_detect_new(mask, value, rectangle_info, color):
    mask_site = np.where(mask>0)#异常颜色像素点的坐标集合
    site_x = mask_site[1]#异常像素点的x坐标
    site_y = mask_site[0]#异常像素点的y坐标，和x是一一对应，并且排序按照y从小到大排
    a = site_y[len(site_y)-1]
    
    a_max = np.where(site_y==a)#求y最大的，也就是最下面轮廓的y
    a_max = a_max[0]
    
    x = site_x[a_max[0]:a_max[len(a_max)-1]]#异常像素点最下面的所有x坐标
    x0 = x[:-1]
    x1 = x[1:]
    sub_x = np.array(x1)-np.array(x0)#做差判断连续性
    sub_x_site = np.where(sub_x>1)
    sub_x_site = sub_x_site[0].tolist()
    sub_x_site.append(-1)
    sub_x_site = [i + 1 for i in sub_x_site]
    tag = x[sub_x_site]
    for i in range(len(tag)):
        y = np.where(site_x==tag[i])       
        y = y[0]       
        h = len(y)
        
        rectangle_info.append([tag[i], h, color, value])
        


def mask_detect(mask, value, rectangle_info, color):
    mask_site = np.where(mask>0)#异常颜色像素点的坐标集合
    site_x = mask_site[1]#异常像素点的x坐标
    site_y = mask_site[0]#异常像素点的y坐标，和x是一一对应，并且排序按照y从小到大排
    upper_line_y_site = np.where(site_y<value) #返回横线之上像素值的y的坐标的坐标
    
    #由于site_y是按照从小到大排序的，所以直接选取前len（upper_line_y_site）部分即为横线之上像素点x的坐标
    unper_line_x = site_x[0:len(upper_line_y_site[0])]
    
    #但是会有很多重复的，因此要去除重复的
    unper_line_x, tag_x = np.unique(unper_line_x, return_index=True)
    
    
    #之后就要查找连续性，要给他分段以判断不同的柱子
    x0 = unper_line_x[:-1]
    x1 = unper_line_x[1:]
    sub_x = np.array(x1)-np.array(x0)#做差判断连续性
    sub_x_site = np.where(sub_x>1)#选取中断点,这个是去除重复后的x的坐标的坐标
    
    
    # if sub_x_site[0]:#不止有一个异常柱子
    for i in range(len(sub_x_site[0])):
        tag = sub_x_site[0][i]
        x = unper_line_x[tag+1]
        y_total = np.where(site_x == x)
        h = len(y_total[0])#高度为当前x有多少个y与之对应

        rectangle_info.append([x, h, color, 1])
    #第一个柱子
    x = unper_line_x[0]
    
    y_total = np.where(site_x == x)
    h = len(y_total[0])
    rectangle_info.append([x, h, color, 1])