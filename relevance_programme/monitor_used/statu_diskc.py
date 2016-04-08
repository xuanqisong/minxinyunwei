#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# [服务器IP, 数据类型, 返回输入参数, shell返回值, 返回错误信息]
import time


def data_execute(li):
    r_li = []
    disk_rs_list = li[3]
    for k in range(0, len(disk_rs_list)):
        if k != 0:
            re_string_list = disk_rs_list[k].split("#")
            ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            total = int(re_string_list[0])
            use = int(re_string_list[1])
            free = int(re_string_list[2])
            # a = (float(use) / float(total)) * 100
            used = int(re_string_list[3].replace("%", ""))
            disk_name = re_string_list[4].replace("\n", "")

            r_li.append([li[0], ti, total, free, use, used, disk_name])

    return r_li
