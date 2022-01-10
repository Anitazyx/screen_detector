
# x 为 420-1700
# y 为 170-420 490-682 775-990
#固定值：整张图片裁剪成3块的位置坐标是固定



import cv2
import numpy as np
import os
import argparse
import time
from time import perf_counter
import sys
sys.path.append("..")
from utils.general import contours_detect, mask_detect, mask_detect_new

import random 
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
 

def random_sort2(n):
    l = [random.random() for i in range(n)]
    l.sort()
    return l


#切分三张柱状图
def crop_src(src, crop_x, crop_y):
    graph_list = []   
    for i in range(0, len(crop_y), 2):
        graph = src[crop_y[i]:crop_y[i+1], crop_x[0]:crop_x[1]]
        graph_list.append(graph)
    return graph_list


#生成对应颜色的掩膜
def find_color(src, color):
    
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    
    return cv2.inRange(hsv, color_dist['lower_'+color], color_dist['upper_'+color])
    
    

#按照x的位置进行排序
def for_x(elem):
    return elem[0]



#计算柱状图的各个数值
def caculate_height(mask, color, value, min_width):

    rectangle_info = []#保存每个柱子的x值（为了排序），和h值（为了计算数值）
    if color=='green':#绿色的检测

        mask_detect_new(mask, 0, rectangle_info, color)
        
        return rectangle_info

    else:#异常颜色的检测，还没有考虑异常颜色落在横线上的情况
        mask_site = np.where(mask>0)#异常颜色像素点的坐标集合
        site_x = mask_site[1]#异常像素点的x坐标
        site_y = mask_site[0]#异常像素点的y坐标，和x是一一对应，并且排序按照y从小到大排
        a = site_y[len(site_y)-1]
        
        a_max = np.where(site_y==a+1)#求y最大的，也就是最下面轮廓的y
        a_max = a_max[0]
        if len(a_max) < min_width:
            # print(color)
            # print("未检测到柱子")
           
            return rectangle_info
  
        x = site_x[a_max[0]:a_max[len(a_max)-1]]#异常像素点最下面的所有x坐标
       
        x0 = x[:-1]
        x1 = x[1:]
        sub_x = x1-x0
        
        sub_x[0] = 1

        # sub_x = np.array(x1)-np.array(x0)#做差判断连续性
        sub_x_site = np.where(sub_x>1)
        sub_x_site = sub_x_site[0].tolist()
        sub_x_site.append(-1)
        for i in range (len(sub_x_site)):
            if sub_x_site[i] == -1:
                sub_x_site[i]+=6
             
                tag = x[sub_x_site[i]]
                y = np.where(site_x==tag)
                y = y[0]       
                h = len(y)
                if h>value*0.8:#高于最低高度，否则是误判柱子                   
                    rectangle_info.append([tag, h, color, 1])
                continue
            elif sub_x[sub_x_site[i]-1] == 1 and sub_x_site[i]+6<len(x):
                sub_x_site[i]+=6               
                tag = x[sub_x_site[i]]
                y = np.where(site_x==tag)
                y = y[0]       
                h = len(y)
                if h>value*0.8:#高于最低高度，否则是误判柱子
                   
                    rectangle_info.append([tag, h, color, 1])
                
            else:
                # sub_x_site[i] = len(x)
                continue
   
        # sub_x_site.append(-1)
        # sub_x_site = [i + 6 for i in sub_x_site]#一定要+1，+5是因为边缘可能存在模糊现象 
        


        # for i in range(len(sub_x_site)):
        #     if sub_x_site[i]<len(x):
        #         tag = x[sub_x_site[i]]
        #         y = np.where(site_x==tag)
        #         y = y[0]       
        #         h = len(y)
        #         if h>value*0.8:#高于最低高度，否则是误判柱子
        #             rectangle_info.append([tag, h, color, 1])
        # tag = x[sub_x_site]
        # for i in range(len(tag)):
        #     y = np.where(site_x==tag[i])      
        #     y = y[0]       
        #     h = len(y)
        #     if h>value*0.8:#高于最低高度，否则是误判柱子
        #         rectangle_info.append([tag[i], h, color, 1])
          
        return rectangle_info

def is_all_black(color_mask):#判断是否是全黑的
    return not(np.any(color_mask))

def get_order_wind(rectangle_info):
    order = []
    for i in range(len(rectangle_info)):
        
        a = 0
        if (rectangle_info[i][0] - 53) > 0:
            a+=1#第二个柱子往后
            a+=int((rectangle_info[i][0]-53)/38)
            
        
        order.append(a)
        
    return order
            

def wind_demo(wind, min_height_dist):
    y = wind.shape[0]
    x = wind.shape[1]
    
    
    wind_detect = wind[int(y*0.75):int(y*0.85), 0:x]# 裁剪出一条做异常检测
    
    rectangle_info = []#保存信息
    
    # green_mask = find_color(wind, 'green')
    # green_info = caculate_height(green_mask, 'green', 0, 20)
    # if green_info is not None:

    #     rectangle_info.extend(green_info)
    
    
    tag_unnormal = 0
    
    
    for color, value in min_height_dist.items():
        
        if not is_all_black(find_color(wind_detect, color)):
            
            
            color_mask = find_color(wind, color)
            cv2.imwrite("orange.jpg", color_mask)
            color_info = caculate_height(color_mask, color, value, 20)
            
            if len(color_info)>0:
                tag_unnormal = 1
                rectangle_info.extend(color_info)
    
    # rectangle_info.sort(key = for_x)
    if len(rectangle_info)<17:
        order_wind = get_order_wind(rectangle_info)
    
   
    if tag_unnormal == 1:
        print("*****存在异常风速*****")
        unnormal=[x[3] for x in rectangle_info]
        unnormal_site = np.where(np.array(unnormal)>0)
        
        for i in iter(unnormal_site[0]):
            print("异常公里标", tag_wind[order_wind[i]])
            color = rectangle_info[i][2]
            
            print("风量警报", wind_jingbao[color])
            wind_speed = (rectangle_info[i][1]/188)*40
            print("风速"+"%.3f" %wind_speed+"m/s")
            print('   ')
        
    # else:
    #     print("风速未见异常")
    if args.show_all:
        for i in range(len(rectangle_info)):
            # print("公里标"+tag_wind[i])
            # color = rectangle_info[i][2]
            # print("风量状态", wind_jingbao[color])
            wind_speed = (rectangle_info[i][1]/188)*40
            # print("风速"+"%.3f" %wind_speed+"m/s")
            print("%.3f" %wind_speed+",")
            # print('   ')


#得到柱子所对应为第几个公里标,100, 170, 240, 310
#默认y轴到边缘距离为5个像素
def get_order(rectangle_info):
    order = []
    for i in range(len(rectangle_info)):
        
        a = 0
        if (rectangle_info[i][0] - 100) > 0:
            a+=1#第二个柱子往后
            a+=int((rectangle_info[i][0]-100)/70)
            
        
        order.append(a)
        
    return order
            


def snow_demo(snow, min_height_dist):
    y = snow.shape[0]
    x = snow.shape[1]
       
    snow_detect = snow[int(y*0.8):int(y*0.9), 0:x]# 裁剪出一条做异常检测
    
    rectangle_info = []#保存信息
    # green_mask = find_color(snow, 'green')
    # green_info = caculate_height(green_mask, 'green', None)
    # rectangle_info.extend(green_info)
   
    
    tag_unnormal = 0
    for color , value in min_height_dist.items():
        
        if not is_all_black(find_color(snow_detect, color)):
            
            color_mask = find_color(snow, color)
            cv2.imwrite("blue.jpg", color_mask)
            color_info = caculate_height(color_mask, color, value, 50)
            if len(color_info)>0:
                tag_unnormal = 1
                rectangle_info.extend(color_info)
    
    rectangle_info.sort(key = for_x)
    
    
    if len(rectangle_info)<17:
        order_snow = get_order(rectangle_info)
    
    
    if tag_unnormal == 1:
        print("*****存在异常雪量*****")
        unnormal=[x[3] for x in rectangle_info]
        unnormal_site = np.where(np.array(unnormal)>0)
        
        for i in iter(unnormal_site[0]):
            print("异常公里标", tag_snow[order_snow[i]])
            color = rectangle_info[i][2]
            
            print("雪深警报", snow_jingbao[color])
            snow_height = (rectangle_info[i][1]/188)*150
            print("雪深"+"%.3f" %snow_height+"mm")
            print('   ')
    # else:
    #     print("雪深未见异常")


def rain_demo(rain, min_height_dist):
    y = rain.shape[0]
    x = rain.shape[1]
    rain_detect = rain[int(y*0.8):int(y*0.85), 0:x]# 裁剪出一条做异常检测
    rectangle_info = []#保存信息
    tag_unnormal = 0
    
    
    for color , value in min_height_dist.items():
        if not is_all_black(find_color(rain_detect, color)):
            
            color_mask = find_color(rain, color)
            cv2.imwrite("dark_blue.jpg", color_mask)
            color_info = caculate_height(color_mask, color, value, 6)
            
            if len(color_info)>0:
                tag_unnormal = 1
                rectangle_info.extend(color_info)
    
    
    
    rectangle_info.sort(key = for_x)
    
    if len(rectangle_info)<17:
        order_rain = get_order(rectangle_info)
    if tag_unnormal == 1:
        print("*****存在异常雨量*****")
        unnormal=[x[3] for x in rectangle_info]
        unnormal_site = np.where(np.array(unnormal)>0)
        for i in iter(unnormal_site[0]):
            print("异常公里标", tag_rain[order_rain[i]])
            color = rectangle_info[i][2]
            
            print("雨量警报", rain_jingbao[color])
            rain_height = (rectangle_info[i][1]/188)*80
            print("雨量"+"%.3f" %rain_height+"mm")
            print('   ')
    # else:
        # print("雨量未见异常")


def main(graph_list):
    #处理风速图   
    wind = graph_list[0]     
    wind_demo(wind, wind_min_height)
    

    
    #处理雨量图
    rain = graph_list[1]
    rain_demo(rain, rain_min_height)

    #处理雪量图
    snow = graph_list[2]
    snow_demo(snow, snow_min_height)
    



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--show_all', action = 'store_true' , help = 'show all message', default = False)
    args = parser.parse_args()

    color_dist = {'lower_blue':np.array([115, 100,100]), 'upper_blue':np.array([125, 255, 255]),
        'lower_dark_blue':np.array([110, 100,100]), 'upper_dark_blue':np.array([115, 255, 255]),
        'lower_green':np.array([50, 100, 100]), 'upper_green':np.array([70, 255, 255]),
        'lower_red':np.array([0, 120, 120]), 'upper_red':np.array([5, 255, 255]),
        'lower_orange':np.array([15, 100, 100]), 'upper_orange':np.array([25, 255, 255]), 
        'lower_yellow':np.array([25, 100, 100]), 'upper_yellow':np.array([35, 255, 255])
    }
    #定义三张柱状图的切分坐标
    crop_x = [420, 1700]
    crop_y = [185, 375, 505, 697, 790, 980]
    
    # print(crop_y)
    
    #不同颜色柱子的最低高度。横线最上面的高度
    wind_min_height = {'blue':68, 'yellow':92, 'orange':115, 'red':139}
    rain_min_height = {'blue':19, 'dark_blue':41, 'yellow':75, 'orange':97, 'red':128}
    snow_min_height = {'blue':65}



    wind_jingbao = {'green':'正常风速', 'blue':'大风一级报警', 'yellow':'大风二级报警', 'orange':'大风三级报警', 'red':'大风停车报警'}
    rain_jingbao = {'blue':'小时雨量报警', 'dark_blue':'连续雨量报警', 'yellow':'雨量二级报警', 'orange':'雨量三级报警', 'red':'雨量停车报警'}
    snow_jingbao = {'green':'正常雪深', 'blue':'雪深一级报警'}

    tag_wind = ['K7+255', 'K17+608', 'K27+756', 'K35+374', 'K44+878', 'K49+844', 'k55+561', 'K64+732', 'K70+546',
                'K76+978', 'K84+596', 'K110+814', 'K114+915', 'K120+609', 'K124+026', 'K130+265', 'K135+191',
                'K140+767', 'K148+770', 'K155+244', 'K168+152', 'K170+903', 'K182+090', 'K187+060', 'K196+280', 
                'K209+060', 'K216+060', 'K225+101', 'K236+632', 'K241+520', 'K251+956', 'K255+190', 'K262+266' ]

    tag_rain = ['K6+004', 'K29+190', 'K44+255', 'K66+855', 'K85+604', 'K92+500', 'K110+884', 'K130+651', 'K140+851', 
                'K155+931', 'K170+690', 'K186+640', 'K196+521', 'K217+301', 'K240+956', 'K253+056', 'K273+956']

    tag_snow = ['K6+905', 'K27+416', 'K44+739', 'K64+271', 'K84+546', 'K93+032', 'K110+941', 'K132+265', 'K140+768', 
                'K155+244', 'K171+656', 'K187+060', 'K209+111', 'K225+697', 'K240+992', 'K252+534', 'K273+131']
    cap = cv2.VideoCapture(0)
    while 1:
        
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) 
        cap.set(cv2.CAP_PROP_FPS, 20)
        
        ret, src = cap.read()
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
        # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # print(fps, width, height)
        print(cap.get(cv2.CAP_PROP_FPS))
        
        
        graph_list = crop_src(src, crop_x, crop_y)
        cv2.imshow('capture', src)
        cv2.imwrite("3.jpg", src )
        
        main(graph_list)
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
    
    cap.release()
    # src = cv2.imread("3.jpg")
    # graph_list = crop_src(src, crop_x, crop_y)
    # main(graph_list)
    
    
        
        

        
        

        
        


    
        
    
   
    

        
        

        
        

        
        


    
        