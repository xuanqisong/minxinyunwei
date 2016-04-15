# -*- coding: utf-8 -*-
import os
from Tools.DBtools import MysqlDb
from home.baseclass import *
from Tools.global_class import Server
from Tools.global_function import encrypt
from Tools import global_value


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
    mysql = MysqlDb('mysql-host')

    sql = "INSERT INTO job_table (t_year,t_month,t_day,t_hour,t_minute,t_second,function_name,run_mark) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    rs_tu = mysql.run_sql(sql, [year_n, month_n, day_n, hour_n, minute_n, second_n, function_dir, '1'])

    if len(rs_tu) == 0:
        return True
    else:
        return False


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


# service manager
def service_detail():
    re_li = []
    mysql = MysqlDb('mysql-host')
    sql = "SELECT * FROM server_list"
    re_tu = mysql.run_sql(sql)
    for tu in re_tu:
        server = Server(tu)
        server.binding_server_value()
        re_li.append(server)
    return re_li


def service_group():
    re_li = []
    mysql = MysqlDb('mysql-host')
    sql = "SELECT DISTINCT(`group`) FROM server_list"
    re_tu = mysql.run_sql(sql)
    for tu in re_tu:
        re_li.append(tu[0])
    return re_li


# 服务器增删改查
# 检验服务器字段
def check_server_field(request, method):
    # 检验重复IP
    server_list = service_detail()
    server_iplist = []
    for old_server in server_list:
        server_iplist.append(old_server.ip)
    # 校对字段
    check_report = {'report': True}
    if method == "new":
        server_ip1 = request.POST.get('server_ip1')
        server_ip2 = request.POST.get('server_ip2')
        server_ip3 = request.POST.get('server_ip3')
        server_ip4 = request.POST.get('server_ip4')

        server_ip = str(server_ip1) + "." + str(server_ip2) + "." + str(server_ip3) + "." + str(server_ip4)
    else:
        server_ip = request.POST.get('server_ip')

    if request.POST.get('server_detail') == '':
        server_detail = "未描述"
    else:
        server_detail = request.POST.get('server_detail')

    if request.POST.get('server_group') == '':
        server_group = 'nogroup'
    else:
        server_group = request.POST.get('server_group')

    server = Server((server_ip, request.POST.get('server_user'),
                     encrypt(global_value.ENCRYPT_KEY_VALUE, request.POST.get('server_password')),
                     request.POST.get('server_port'), server_detail,
                     server_group, request.POST.get('server_state'), request.POST.get('server_type')))
    server.binding_server_value()
    # check ip
    if method == "new":
        if server_ip in server_iplist:
            check_report['server_ip'] = "此服务器已存在"
            check_report['report'] = False

        if server_ip1 == '' or server_ip2 == '' or server_ip3 == '' or server_ip4 == '':
            check_report['server_ip'] = "IP不可为空"
            check_report['report'] = False

    # check_server_user
    if server.user == '':
        check_report['server_user'] = "服务器用户名不可为空"
        check_report['report'] = False

    # check_server_user
    if method == "change":
        if not check_old_password(server_ip,
                                  encrypt(global_value.ENCRYPT_KEY_VALUE, request.POST.get('server_password_o'))):
            check_report['server_password_o'] = "旧服务密码输入错误"
            check_report['report'] = False

    if server.password == '':
        check_report['server_password'] = "密码不能为空"
        check_report['report'] = False

    if encrypt(global_value.ENCRYPT_KEY_VALUE, request.POST.get('server_password_t')) != server.password:
        check_report['server_password_t'] = "两次输入的密码不同"
        check_report['report'] = False

    # check_server_port
    if server.port == '':
        check_report['server_port'] = "端口号不能为空"
        check_report['report'] = False

    check_report['server'] = server

    return check_report


# 插入修改server信息
def insert_server(server):
    mysql = MysqlDb('mysql-host')
    server_list = server.value_list
    value_list = (server.user, server.password, int(server.port), server.detail,
                  server.group,
                  int(server.status), server.servertype)
    sql = "insert into server_list values(%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update user=%s,password=%s,port=%s,detail=%s,`group`=%s,status=%s,servertype=%s"
    l_count = mysql.run_uid(sql, server_list + value_list)
    if l_count > 0:
        return True
    else:
        return False


def check_old_password(ip, pas):
    mysql = MysqlDb('mysql-host')
    sql = "select count(1) from server_list where ip=%s and password=%s"
    rs_tu = mysql.run_sql(sql, [ip, pas])
    if rs_tu[0][0] > 0:
        return True
    else:
        return False


def call_procedure(procedure_name, methon, table_name):
    mysql = MysqlDb('mysql-host')
    mysql.get_connect()
    cur = mysql.conn.cursor()
    if methon == 'new':
        cur.callproc(procedure_name, (table_name,))
    else:
        cur.callproc(procedure_name, (table_name,))
    return True


def read_service(ip):
    mysql = MysqlDb('mysql-host')
    sql = "select * from server_list where ip = %s"
    rs_tu = mysql.run_sql(sql, ip)
    server = Server(rs_tu[0])
    server.binding_server_value()
    return server


def delete_bak_server(server_ip_list):
    mysql = MysqlDb('mysql-host')
    ip_list = ''
    for ip in server_ip_list:
        ip_list = ip_list + "'" + ip + "',"
    sql = "insert into server_list_bak SELECT *,now() from server_list where ip in (" + ip_list[:-1] + ")"
    l_count = mysql.run_uid(sql)
    if l_count > 0:
        sql = "delete from server_list where ip in (" + ip_list[:-1] + ")"
        ll_count = mysql.run_uid(sql)
        if ll_count > 0:
            return True
        else:
            return False
    else:
        return False


def get_status_table():
    mysql = MysqlDb('mysql-host')
    sql = "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'minxinyunwei' AND table_name like 'stat%'"
    re_tu = mysql.run_sql(sql)
    return re_tu
