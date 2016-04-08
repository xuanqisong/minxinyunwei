#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# [服务器IP, 数据类型, 返回输入参数, shell返回值, 返回错误信息]
import time


def data_execute(li):
    ip = li[0]
    ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    s_list = li[3].split("#")
    total = int(s_list[0])
    free = int(s_list[2])
    cached = int(s_list[3])
    use = total - free - cached
    a = (float(use) / float(total)) * 100
    used = ("%.2f" % a)

    return [li[0], ti, total, use, free, used]
