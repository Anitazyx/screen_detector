#!/usr/bin/env python2
# # coding: utf8
# import multiprocessing
# from multiprocessing.context import Process

# def foo(h,context):
#     for h in range(18):
#         if h%2 == 0:
#             print (h)
#         else:
#             context.append(h)
# def foo2(a, context):
#     print(context)

# if __name__ == "__main__":
#     ## 设置共享list
#     con = multiprocessing.Manager().list()
#     ## 设置进程池大小
  
#     # con = multiprocessing.Manager().list()
#     p1 = Process(target=foo, args=(0, con))
#     p2 = Process(target=foo2, args=(0, con))
  
#     p1.start()
#     p2.start()

#     p1.join()
#     p2.join()
#     # print (con)
    


#encoding:utf-8
from multiprocessing import Process
import multiprocessing
import os, time, random

#线程启动后实际执行的代码块
def r1(process_name,message_now):
    for i in range(5):
        message_now.append(1)
        print (process_name, os.getpid()    ) #打印出当前进程的id
        time.sleep(random.random())
        # time.sleep(random.random())

def r2(process_name,message_now):
    while 1:
        print(process_name)
        print(message_now)
    # for i in range(5):
    #     message_now.append(2)
    #     print (process_name, os.getpid())     #打印出当前进程的id
    #     time.sleep(random.random())
    #     time.sleep(random.random())
    #     print(message_now) 
    
if __name__ == "__main__":
        print ("main process run...")
        message_now = multiprocessing.Manager().list()
        p1 = Process(target=r1, args=('process_name1', message_now)) #target:指定进程执行的函数，args:该函数的参数，需要使用tuple
             
        p2 = Process(target=r2, args=('process_name2', message_now))
        
        p1.start()    #通过调用start方法启动进程，跟线程差不多。
        
        p2.start()    #但run方法在哪呢？待会说。。。
        p1.join()     #join方法也很有意思，寻思了一下午，终于理解了。待会演示。
        
        p2.join()
       
        print ("main process runned all lines...")