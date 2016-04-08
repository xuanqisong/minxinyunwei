# -*- coding: utf-8 -*-
import os
from Tools.DBtools import MysqlDb
from home.baseclass import *


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


# 获取job信息
def job_message():
    mysql = MysqlDb('mysql-host')
    sql = "SELECT * FROM job_table"
    re_tuple = mysql.run_sql(sql)
    re_li = []
    for tu in re_tuple:
        job = TableJob(tu)
        job.binding_value()
        re_li.append(job)
    return re_li


def insert_jobmessage(function_name, year_n, month_n, day_n, hour_n, minute_n, second_n):
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    function_dir = dir_path + "/relevance_programme/" + function_name
    combine_time = change_time_value(year_n, month_n, day_n, hour_n, minute_n, second_n)
    mysql = MysqlDb('mysql-host')

    sql = "INSERT INTO job_table (t_year,t_month,t_day,t_hour,t_minute,t_second,combine_time,function_name,run_mark) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    rs_tu = mysql.run_sql(sql, [year_n, month_n, day_n, hour_n, minute_n, second_n, combine_time, function_dir, '1'])

    if len(rs_tu) == 0:
        return True
    else:
        return False


def change_time_value(year_n, month_n, day_n, hour_n, minute_n, second_n):
    combine_time = ''
    if year_n != '':
        combine_time += year_n + month_n.rjust(2, "0") + day_n.rjust(2, "0") + hour_n.rjust(2, "0") + minute_n.rjust(2,
                                                                                                                     "0") + second_n.rjust(
                2, "0")
    elif month_n != '':
        combine_time += month_n.rjust(2, "0") + day_n.rjust(2, "0") + hour_n.rjust(2, "0") + minute_n.rjust(2,
                                                                                                            "0") + second_n.rjust(
                2, "0")
    elif day_n != '':
        combine_time += day_n.rjust(2, "0") + hour_n.rjust(2, "0") + minute_n.rjust(2, "0") + second_n.rjust(2, "0")
    elif hour_n != '':
        combine_time += hour_n.rjust(2, "0") + minute_n.rjust(2, "0") + second_n.rjust(2, "0")
    elif minute_n != '':
        combine_time += minute_n.rjust(2, "0") + second_n.rjust(2, "0")
    else:
        combine_time += second_n.rjust(2, "0")

    return combine_time


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


def change_run_mark(pid, run_mark):
    mysql = MysqlDb('mysql-host')
    if run_mark == '1':
        run_markn = '0'
    elif run_mark == '0':
        run_markn = '1'
    # sql = "UPDATE job_table SET run_mark = '" + run_mark + "' WHERE id= '" + pid + "'"
    sql = "UPDATE job_table SET run_mark = %s WHERE id = %s"
    count = mysql.run_uid(sql, [run_markn, pid])
    if count > 0:
        return [True, run_markn]
    else:
        return [False, run_mark]


def delete_job(pid):
    mysql = MysqlDb('mysql-host')
    sql = "DELETE FROM job_table WHERE id = %s"
    count = mysql.run_uid(sql, [pid])
    if count > 0:
        return True
    else:
        return False
