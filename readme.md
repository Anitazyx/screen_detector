## 屏幕检测算法

###### 1. 检测本地视频进行异常检测，并发送邮件

```
    python demo/demo_mutil.py
```

###### 2. 实时检测屏幕异常，并发送邮件

```
    python demo/demo_online_mutil.py
```
###### 3. 输入一张图片或图片文件夹进行异常检测，并输出结果

```
    python ppl/screen_detector.py #带运行时间检测
    
    python ppl/screen_detector_cupy.py #使用cupy代替numpy
```



###### 4. 其他脚本
-  对于指定图像生成对应颜色的掩膜并保存
```
    python tools/main.py
```

- 数字裁剪脚本（水平与垂直），首先需要对柱子上面的小数进行裁剪，之后再运行此脚本，输出的是单个数字的二值化图像

```
    python tools/number.py
```
- 识别数字脚本，输入数字二值化图像，使用直方图投影得到数字特征，计算输入与0-10之间的余弦相似性，得到数字结果

```
    python tools/histogram_match.py
```
- 使用matplotlib画图，伪造批量数据

```
    python tools/draw.py
```
- 将图像序列合成视频

```
    python tools/pic2video.py
```
---




