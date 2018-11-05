# -*- coding: utf-8 -*-

from RPi import GPIO
import time

# 超过60度启动
upper_temp = 60
# 低于40度关闭
lower_temp = 40

# 采用BCM引脚编号
GPIO.setmode(GPIO.BCM)
# 关闭警告
GPIO.setwarnings(False)
# 控制三级管的GPIO编号
channel = 18
# 初始GPIO输出高电平, 风扇不转
GPIO.setup(channel, GPIO.OUT, initial = GPIO.HIGH)

# 获取树莓派温度的函数
def get_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as fp:
        return int(fp.read()) / 1000

# 进入检测
try:
    while True:
        # 获取当前温度
        temp = get_temp()
        # 如果大于上限, 则给低电平, 闭合三极管
        if temp >= upper_temp:
            GPIO.output(channel, GPIO.LOW)
        elif temp < lower_temp: # 低于下限, 则给高电平, 断开三极管
            GPIO.output(channel, GPIO.HIGH)
        # 每隔10秒检测1次
        time.sleep(10)
except Exception, e:
    print(e)

# 重置GPIO状态
GPIO.cleanup()
