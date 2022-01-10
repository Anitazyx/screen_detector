#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 18:07
# @Author  : YuZJ
# @Email   : yuzj@jxresearch.com
# @File    : mail.py

import cv2
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from mimetypes import guess_type
import time

class warn_info():
    def __init__(self, type, level, tag, result):
        self.type = type
        self.level = level
        self.tag = tag
        self.result = result

class warn_message():
    def __init__(self, wind_info, rain_info, snow_info):
        self.wind_info = wind_info
        self.rain_info = rain_info
        self.snow_info = snow_info

class MyEmail():

    def __init__(self, sender, receivers, subject):
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
    def send_alarm(self, img, info):

        msgRoot = MIMEMultipart('related')

        msgRoot['From'] = Header(self.sender, 'utf-8')
        # 支持多人接收
        msgRoot['To'] = ','.join(self.receivers)

        msgRoot['Subject'] = Header(self.subject, 'utf-8')

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        # mail_msg = """
        # <p>type:  </p>
        # <p>图片演示：</p>
        # <p><img height=480 width=640 src="cid:image1"></p>
        # """
        mail_msg = '<p>报警类型:%s</p><p>图片演示：</p><p><img height=480 width=640 src="cid:image1"></p>'%(info)

        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        # 指定图片为当前目录

        #以文件形式读取的图片
        # (mimetype, encoding) = guess_type(img)
        # (maintype, subtype) = mimetype.split('/')
        # fp = open(img, 'rb')
        # msgImage = MIMEImage(fp.read(), **{'_subtype': subtype})
        # fp.close()

        #发送opencv读取的图片
        image = cv2.imread(img)
        img_encode = cv2.imencode('.jpg', image)[1].tobytes()
        msgImage = MIMEImage(img_encode, **{'_subtype': 'jpeg'})

        # 定义图片 ID，在 HTML 文本中引用
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        try:
            smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
            smtpObj.login(self.sender, 'STOIKEJQGLKQQSPB')
            smtpObj.sendmail(self.sender, self.receivers, msgRoot.as_string())
            print('邮件发送成功')
        except smtplib.SMTPException as ex:
            print('Error: 无法发送邮件')
            print(ex)
        
    def send_message(self, warn_message, now_time, src):
    
        msgRoot = MIMEMultipart('related')

        #定义发送者，接收者，标题
        msgRoot['From'] = Header(self.sender, 'utf-8')
        # 支持多人接收
        msgRoot['To'] = ','.join(self.receivers)

        msgRoot['Subject'] = Header(self.subject, 'utf-8')

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        
        
        if warn_message.wind_info is not None:
            
            for i in range (len(warn_message.wind_info.tag)):
                wind_msg = """          
                    <p>风速警报：%s</p><p>异常公里标：%s</p><p>报警风速:%.3f</p><p>-------------------------</p>  
                """%((warn_message.wind_info.level[i]),(warn_message.wind_info.tag[i]),(warn_message.wind_info.result[i]))
                msgAlternative.attach(MIMEText(wind_msg, 'html', 'utf-8'))

        if warn_message.rain_info is not None:
            
            for i in range (len(warn_message.rain_info.tag)):
                rain_msg = """          
                    <p>雨量警报：%s</p><p>异常公里标：%s</p><p>报警雨量:%.3f</p><p>-------------------------</p>
                """%((warn_message.rain_info.level[i]),(warn_message.rain_info.tag[i]),(warn_message.rain_info.result[i]))
                msgAlternative.attach(MIMEText(rain_msg, 'html', 'utf-8'))

        if warn_message.snow_info is not None:
            
            for i in range (len(warn_message.snow_info.tag)):
                snow_msg = """          
                    <p>雪量警报：%s</p><p>异常公里标：%s</p><p>报警雪量:%.3f</p><p>-------------------------</p>
                """%((warn_message.snow_info.level[i]),(warn_message.snow_info.tag[i]),(warn_message.snow_info.result[i]))
                msgAlternative.attach(MIMEText(snow_msg, 'html', 'utf-8'))
        
        title = """
        <p>检测时间：%s</p></p><p><img height=480 width=640 src="cid:image1"></p>'
        """%(now_time)
        msgAlternative.attach(MIMEText(title, 'html', 'utf-8'))

        
        #发送opencv读取的图片
        
        img_encode = cv2.imencode('.jpg', src)[1].tobytes()
        msgImage = MIMEImage(img_encode, **{'_subtype': 'jpeg'})

        # 定义图片 ID，在 HTML 文本中引用
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)
     
        
        try:
            s = time.time()
            smtpObj = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
            smtpObj.login(self.sender, 'Jiaxun123')
            smtpObj.sendmail(self.sender, self.receivers, msgRoot.as_string())
            print('邮件发送成功')
            
        except smtplib.SMTPException as ex:
            print('Error: 无法发送邮件')
            print(ex)


    def send_message_list(self, warn_message,src):
        
        msgRoot = MIMEMultipart('related')

        #定义发送者，接收者，标题
        msgRoot['From'] = Header(self.sender, 'utf-8')
        # 支持多人接收
        msgRoot['To'] = ','.join(self.receivers)

        msgRoot['Subject'] = Header(self.subject, 'utf-8')

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        
     
        
        if warn_message[0] is not None:   
    
            for i in range (len(warn_message[0][1])):
                wind_msg = """          
                    <p>风速警报：%s</p><p>异常公里标：%s</p><p>报警风速:%.3f</p><p>-------------------------</p>  
                """%((warn_message[0][0][i]),(warn_message[0][1][i]),(warn_message[0][2][i]))
                msgAlternative.attach(MIMEText(wind_msg, 'html', 'utf-8'))

        if warn_message[1] is not None:
            
            for i in range (len(warn_message[1][1])):
                rain_msg = """          
                    <p>雨量警报：%s</p><p>异常公里标：%s</p><p>报警雨量:%.3f</p><p>-------------------------</p>
                """%((warn_message[1][0][i]),(warn_message[1][1][i]),(warn_message[1][2][i]))
                msgAlternative.attach(MIMEText(rain_msg, 'html', 'utf-8'))

        if warn_message[2] is not None:
            
            for i in range (len(warn_message[2][1])):
                snow_msg = """          
                    <p>雪量警报：%s</p><p>异常公里标：%s</p><p>报警雪量:%.3f</p><p>-------------------------</p>
                """%((warn_message[2][0][i]),(warn_message[2][1][i]),(warn_message[2][2][i]))
                msgAlternative.attach(MIMEText(snow_msg, 'html', 'utf-8'))
        
        title = """
        <p>异常状态截图：</p><p><img height=480 width=640 src="cid:image1"></p>'
        """
        msgAlternative.attach(MIMEText(title, 'html', 'utf-8'))

        
        #发送opencv读取的图片
        
        img_encode = cv2.imencode('.jpg', src)[1].tobytes()
        msgImage = MIMEImage(img_encode, **{'_subtype': 'jpeg'})

        # 定义图片 ID，在 HTML 文本中引用
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)
        
        
        try:
            s = time.time()
            smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
            smtpObj.login(self.sender, 'STOIKEJQGLKQQSPB')
            smtpObj.sendmail(self.sender, self.receivers, msgRoot.as_string())
            print('邮件发送成功')
            
        except smtplib.SMTPException as ex:
            print('Error: 无法发送邮件')
            print(ex)
            


if __name__ == "__main__":
    sender = 'ai@jxresearch.com'
    receivers = ['yzj<zhaoyx@jxresearch.com>']
    subject = '屏幕检测'
    start = time.time()
    email_test = MyEmail(sender, receivers, subject)
    end = time.time()
    print(end - start)
    image = "src.jpg"
    email_test.send_alarm(image, '正常')