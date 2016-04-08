# -*- coding: utf-8 -*-
from antivirus.baseclass import *
from Tools.DBtools import MysqlDb
from Tools import global_function
import os

import time
import json


def one_times(ip, scan_type, scan_file):
    re_di = {}
    currp = Scan(ip, scan_type, scan_file)
    currp.start()
    currp.join()
    re_di[ip] = currp.connstr + " " + currp.scanresult
    return re_di


def get_server_group():
    sql = "SELECT DISTINCT(`group`) FROM server_list"
    mysql = MysqlDb('mysql-host')

    rs_tu = mysql.run_sql(sql, '')
    rs_li = global_function.tuple_to_list(rs_tu)

    return rs_li


def get_group_serveripname(group_name):
    sql = "select ip FROM server_list WHERE `group` = %s "

    mysql = MysqlDb('mysql-host')

    rs_tu = mysql.run_sql(sql, [group_name])
    rs_li = global_function.tuple_to_list(rs_tu)

    return rs_li


def get_ip_dir(dir_hole_name):
    ip_dir_di = {}
    for li in dir_hole_name:
        str_list = li.split(":")
        if str_list[0] not in ip_dir_di:
            ip_dir_di[str_list[0]] = [str_list[1]]
        else:
            ip_dir_di[str_list[0]].append(str_list[1])

    return ip_dir_di


def get_ip_clamav(scan_type, ip_dir_di):
    ip_clamav_list = []
    for ip in ip_dir_di:
        clamav = ClamAV(ip, scan_type)
        ip_clamav_list.append(clamav)

    return ip_clamav_list


def check_rsclamavstr(str):
    di_str = eval(str)
    print type(di_str)
    print di_str
    return str


# clamavrun
def start_clamav():
    # 开始
    di = {'message': "start"}
    di_str = json.dumps(di)

    time.sleep(3)
    return di_str


def connect_clamav(clamavlist):
    for clamav in clamavlist:
        clamav.get_cns()
    di = {'message': "get server connect!"}
    for clamav in clamavlist:
        ip_name = str(clamav.ip).replace('.', '')
        file_name = str(clamav.file).replace('/', '')
        if clamav.cns.ping():
            di[ip_name + file_name] = '1'
        else:
            di[ip_name + file_name] = '4'
    di_str = json.dumps(di)
    time.sleep(3)
    return di_str


def start_clamav_thread(clamavlist):
    di = {'message': "is checking!"}
    for clamav in clamavlist:
        ip_name = str(clamav.ip).replace('.', '')
        file_name = str(clamav.file).replace('/', '')
        if clamav.cns.ping():
            clamav.start()
            di[ip_name + file_name] = '2'
    di_str = json.dumps(di)
    time.sleep(3)
    return di_str


def while_check_over(clamavlist):
    check_thread_list = []
    return_tf = False
    di = {'message': ''}
    for clamav in clamavlist:
        ip_name = str(clamav.ip).replace('.', '')
        file_name = str(clamav.file).replace('/', '')
        check_thread_list.append(clamav.is_alive())
        if clamav.is_alive():
            di[ip_name + file_name] = '2'
            di['message'] += clamav.ip + ": is checking! </br>"
        else:
            di[ip_name + file_name] = '3'
            di['message'] += clamav.ip + ": " + check_rsclamavstr(clamav.scanresult) + "</br>"

    di_str = json.dumps(di)
    if True not in check_thread_list:
        return_tf = True
    return [di_str, return_tf]


def end_clamav():
    di = {'message': 'check down!'}
    di_str = json.dumps(di)
    return di_str


def stop_antivirus(clamanlist):
    di = {}
    for clamav in clamanlist:
        ip_name = str(clamav.ip).replace('.', '')
        file_name = str(clamav.file).replace('/', '')
        clamav.shutdown()
        di[ip_name + file_name] = '5'
        di['message'] += clamav.ip + ": antivirus shutdown! </br>"

    di_str = json.dumps(di)
    return di_str


def get_file_data():
    dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_file_di = {}
    # 进入备份路径
    dir_name += '/relevance_programme'
    if not os.path.isdir(dir_name):
        return False

    dir_list = os.listdir(dir_name)
    for file_dir_name in dir_list:
        dir_file_di[file_dir_name] = os.listdir(dir_name + '/' + file_dir_name)

    # 拼接页面data
    data = '['
    for file_dir_name, file_list in dir_file_di.items():
        data += '{ '
        data += 'text: "' + file_dir_name + '",'
        data += 'selectable: false,'
        data += 'nodes:['
        for file_name in file_list:
            if str(file_name).split('.')[1] == 'py':
                data += '{'
                data += 'text: "' + file_name + '",'
                data += '},'
        data = data[:-1]
        data += ']'
        data += '},'

    data = data[:-1]
    data += ']'

    return data


def get_job_detail(f_dir_name):
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_f_path = dir_path + "/relevance_programme/" + f_dir_name
    dir_readme_path = dir_f_path + "/readme.txt"
    if os.path.isfile(dir_readme_path):
        with open(dir_readme_path) as f:
            job_detail = f.read()
    else:
        try:
            with open(dir_readme_path) as f:
                f.read()
        except Exception as e:
            job_detail = str(e)

    return {'job_detail': job_detail}



