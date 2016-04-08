#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# [服务器IP, 数据类型, 返回输入参数, shell返回值, 返回错误信息]
import time


def data_execute(li):
    ip = li[0]
    ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    a = float(li[3][:-4])
    used = ("%.2f" % a)
    return [ip, ti, used]
