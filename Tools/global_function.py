# -*- coding: utf-8 -*-
# !/usr/bin/python
import ConfigParser
import time
import random
import datetime


# 系统公共函数
# 写文件日志函数
def write_file(filepath, txt, method):
    try:
        f = open(filepath, method)
        if isinstance(txt, tuple):
            for va in txt:
                f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(va))
                f.write(' ')
        elif isinstance(txt, list):
            for va in txt:
                f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(va))
                f.write(' ')
        elif isinstance(txt, dict):
            for va in txt.iteritems():
                f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(va[0]))
                f.write(': ')
                f.write(str(va[1]))
                f.write(' ')
        else:
            f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(txt))
            f.write(' ')
        f.write('\n')
        f.close()
    except Exception as e:
        print "write file error :", txt
        print "file path :", filepath
        print "error message :", e


# tuple 转换成list函数
def tuple_to_list(tu):
    li = []
    for va1 in tu:
        if isinstance(va1, tuple):
            li.append(tuple_to_list(va1))
        else:
            li.append(change_utf8(va1))
    return li


# 转码函数
def change_utf8(string):
    try:
        txt = str(string).encode("utf-8")
    except Exception:
        txt = string
    return txt


# 读取配置文件函数
def read_ini(path, target=None):
    cfp = ConfigParser.ConfigParser()
    cfp.read(path)
    di = {}
    if target is not None:
        for se in cfp.sections():
            if se == target:
                for va in cfp.items(se):
                    di[va[0]] = va[1]
    else:
        for se in cfp.sections():
            va_di = {}
            for va in cfp.items(se):
                va_di[va[0]] = va[1]
            di[se] = va_di
    return di


# 随机获取颜色
def get_color(num):
    rt_color_list = []
    color_list = ['#750000', '#EA0000', '#820041', '#FF0080', '#ff7575', '#ffaad5', '#750075', '#FF00FF', '#ffa6ff',
                  '#4B0091', '#9F35FF', '#DCB5FF', '#0000C6', '#4A4AFF', '#CECEFF', '#004B97', '#0080FF', '#84C1FF',
                  '#009393', '#00E3E3', '#019858', '#02F78E', '#96FED1', '#00A600', '#00EC00', '#93FF93',
                  '#64A600', '#9AFF02', '#737300', '#F9F900', '#977C00', '#EAC100', '#FFDC35',
                  '#FFED97', '#BB5E00', '#FF9224', '#FFBB77', '#A23400', '#FF5809', '#FFAD86', '#743A3A', '#AD5A5A',
                  '#CF9E9E', '#808040', '#AFAF61', '#C2C287', '#408080', '#6FB7B7', '#A3D1D1', '#5151A2', '#9999CC',
                  '#7E3D76', '#AE57A4', '#D2A2CC']
    for i in range(0, num):
        rt_color_list.append(random.choice(color_list))
    return rt_color_list


# 获取某年第几周有哪些天
def get_di_week_time(year):
    re_di = {}
    date_start = datetime.datetime(year, 1, 1)
    date_end = datetime.datetime(year, 12, 31)
    date_now = date_start
    while date_end > date_now:
        week_num = date_now.strftime('%W')
        if week_num in re_di:
            re_di[week_num].append(str(date_now))
        else:
            re_di[week_num] = [str(date_now)]

        date_now = date_now + datetime.timedelta(1)

    return re_di


# 字符串加密算法
def encrypt(key, s):
    b = bytearray(str(s).encode("utf8"))
    # 求出 b 的字节数
    n = len(b)
    c = bytearray(n * 2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key  # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16  # b2 = c2*16 + c1
        c1 += 65
        c2 += 65  # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j + 1] = c2
        j += 2

    return c.decode("utf8")


# 字符串反加密算法
def decrypt(key, s):
    c = bytearray(str(s).encode("gbk"))
    n = len(c)  # 计算 b 的字节数
    if n % 2 != 0:
        return ""
    n //= 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j + 1]
        j += 2
        c1 -= 65
        c2 -= 65
        b2 = c2 * 16 + c1
        b1 = b2 ^ key
        b[i] = b1
    try:
        return b.decode("gbk")
    except:
        return "failed"


# job
def str_just(li):
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime("%Y/%m/%d/%H/%M/%S")
    year = now_time.strftime("%Y")
    month = now_time.strftime("%m")
    day = now_time.strftime("%d")
    hour = now_time.strftime("%H")
    minute = now_time.strftime("%M")
    second = now_time.strftime("%S")

    ti_list = []
    if li[0] == "*":
        ti_list.append(year)
    else:
        ti_list.append(li[0])

    if li[1] == "*":
        ti_list.append(month)
    else:
        ti_list.append(li[1])

    if li[2] == "*":
        ti_list.append(day)
    else:
        ti_list.append(li[2])

    if li[3] == "*":
        ti_list.append(hour)
    else:
        ti_list.append(li[3])

    if li[4] == "*":
        ti_list.append(minute)
    else:
        ti_list.append(li[4])

    if li[5] == "*":
        ti_list.append(second)
    else:
        ti_list.append(li[5])

    ti = '/'.join(ti_list)
    return [ti, now_time_str, li[6]]


def judge_time(li):
    check_run = []
    job_ti = str(li[0]).split('/')
    run_ti = str(li[1]).split('/')

    for index, ti in enumerate(job_ti):
        if job_ti[index] == run_ti[index]:
            check_run.append(True)
        else:
            if run_ti[index] in str(job_ti[index]).split(","):
                check_run.append(True)
            else:
                check_run.append(False)
    if False in check_run:
        return False
    else:
        return True
