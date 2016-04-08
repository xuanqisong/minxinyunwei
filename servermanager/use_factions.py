# -*- coding: utf-8 -*-
from Tools import global_function
from Tools.DBtools import MysqlDb
import os

from servermanager.baseclass import *


# 获取IP段
def get_ipsection():
    mysql = MysqlDb('mysql-host')
    sql = "SELECT DISTINCT(SUBSTRING_INDEX(ip,'.',3)) FROM equipment_ip_belong"

    re_tu = mysql.run_sql(sql, '')
    re_li = global_function.tuple_to_list(re_tu)
    return_li = []
    for li in re_li:
        return_li.append(li[0])

    return return_li


# 获取IP段内IP列表

def get_ipinsectionip(section_ip):
    re_di = {}
    mysql = MysqlDb('mysql-host')
    for ip_section in section_ip:
        sql = "SELECT ip FROM equipment_ip_belong WHERE SUBSTRING_INDEX(ip,'.',3)= %s"
        re_tu = mysql.run_sql(sql, ip_section)
        re_li = global_function.tuple_to_list(re_tu)

        for li in re_li:
            if ip_section in re_di:
                re_di[ip_section].append(li[0])
            else:
                re_di[ip_section] = [li[0]]

    return re_di


# 获取ServerIpJtopo列表
def get_serveripjtopolist(ipsection_ip_di):
    re_di = {}
    # 获取ip段内全部IP
    for ip_section, ip_list in ipsection_ip_di.items():
        serveripjtopo_li = []
        hole_ip_li = hole_ip(ip_section)
        for ip in hole_ip_li:
            if ip in ip_list:
                serveripjtopo_li.append(ServerIpJtopo(ip, "1"))
            else:
                serveripjtopo_li.append(ServerIpJtopo(ip, "0"))
        re_di[ip_section] = serveripjtopo_li

    return re_di


# 获取ip段内全部IP
def hole_ip(ip_section):
    re_li = []
    for i in range(1, 255):
        re_li.append(ip_section + "." + str(i))
    return re_li


# 获取服务器列表
def get_serverlist():
    sql_server_list = "select * from server_list WHERE servertype='2'"

    mysql = MysqlDb('mysql-host')

    rs_tu = mysql.run_sql(sql_server_list, '')
    rs_li = global_function.tuple_to_list(rs_tu)

    servernamelist = []

    for li in rs_li:
        a = Server(li[0], li[1], li[2], li[3], li[4], li[5], li[6])
        servernamelist.append(a)

    return servernamelist


# 获取服务器，组别列表
def get_server_grouplist():
    sql = "SELECT DISTINCT(`group`) FROM server_list WHERE  servertype='2'"

    mysql = MysqlDb('mysql-host')
    rs_tu = mysql.run_sql(sql, '')
    rs_li = global_function.tuple_to_list(rs_tu)
    return rs_li


# 服务器增删改查
# 检验服务器字段
def check_server_field(request, method):
    # 检验重复IP
    server_list = get_serverlist()
    server_iplist = []
    for old_server in server_list:
        server_iplist.append(old_server.get_ip())
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
        server_detail = server_ip
    else:
        server_detail = request.POST.get('server_detail')

    if request.POST.get('server_group') == '':
        server_group = 'test'
    else:
        server_group = request.POST.get('server_group')

    server = Server(server_ip, request.POST.get('server_user'), request.POST.get('server_password'),
                    request.POST.get('server_port'), server_detail,
                    server_group, request.POST.get('server_state'))
    # check ip
    if method == "new":
        if server_ip in server_iplist:
            check_report['server_ip'] = "此服务器已存在"
            check_report['report'] = False

        if server_ip1 == '' or server_ip2 == '' or server_ip3 == '' or server_ip4 == '':
            check_report['server_ip'] = "IP不可为空"
            check_report['report'] = False

    # check_server_user
    if server.get_user() == '':
        check_report['server_user'] = "服务器用户名不可为空"
        check_report['report'] = False

    # check_server_user
    if method == "change":
        if not check_old_password(server_ip, request.POST.get('server_password_o')):
            check_report['server_password_o'] = "旧服务密码输入错误"
            check_report['report'] = False

    if server.get_password() == '':
        check_report['server_password'] = "密码不能为空"
        check_report['report'] = False

    if request.POST.get('server_password_t') != server.get_password():
        check_report['server_password_t'] = "两次输入的密码不同"
        check_report['report'] = False

    # check_server_port
    if server.get_port() == '':
        check_report['server_port'] = "端口号不能为空"
        check_report['report'] = False

    check_report['server'] = server

    return check_report


# 插入修改server信息
def insert_server(server):
    mysql = MysqlDb('mysql-host')
    server_list = [server.get_ip(), server.get_user(), server.get_password(), int(server.get_port()),
                   server.get_detail(),
                   server.get_group(), int(server.get_state())]
    value_list = [server.get_user(), server.get_password(), int(server.get_port()), server.get_detail(),
                  server.get_group(),
                  int(server.get_state())]
    sql = "insert into server_list values(%s,%s,%s,%s,%s,%s,%s,'2') on duplicate key update user=%s,password=%s,port=%s,detail=%s,`group`=%s,state=%s,servertype='2'"
    rs_tu = mysql.run_sql(sql, server_list + value_list)
    if len(rs_tu) == 0:
        return True
    else:
        return False


# 删除指定IP，非删除，将IP备份的备份表中
def delete_bak_server(server_ip_list):
    mysql = MysqlDb('mysql-host')
    ip_list = ''
    for ip in server_ip_list:
        ip_list = ip_list + "'" + ip + "',"
    sql = "insert into server_list_bak SELECT *,now() from server_list where ip in (" + ip_list[:-1] + ")"
    rs_tu = mysql.run_sql(sql, '')
    if len(rs_tu) == 0:
        sql = "delete from server_list where ip in (" + ip_list[:-1] + ")"
        rs_tu = mysql.run_sql(sql, '')
        if len(rs_tu) == 0:
            return True
        else:
            return False
    else:
        return False


# 修改指定服务器参数
def read_server(ip):
    mysql = MysqlDb('mysql-host')
    sql = "select * from server_list where ip = %s"
    rs_tu = mysql.run_sql(sql, ip)
    rs_li = global_function.tuple_to_list(rs_tu)
    for li in rs_li:
        server = Server(li[0], li[1], li[2], li[3], li[4], li[5], li[6])

    return server


def check_old_password(ip, pas):
    mysql = MysqlDb('mysql-host')
    sql = "select count(*) from server_list where ip=%s and password=%s"
    rs_tu = mysql.run_sql(sql, [ip, pas])
    if rs_tu[0][0] > 0:
        return True
    else:
        return False


def call_procedure(procedure_name, methon, table_name):
    mysql = MysqlDb('mysql-host')
    conn = mysql.get_connect()
    cur = conn.cursor()
    if methon == 'new':
        cur.callproc(procedure_name, (table_name,))
    else:
        cur.callproc(procedure_name, (table_name,))
    data = cur.fetchall()
    return True


# 获取文件序列
def get_file_data():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    dir_file_di = {}
    # 进入备份路径
    dir_name += '/routerbakfile'

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
            data += '{'
            # data += 'text: "<a href="javascript: clickfile()">'+file_name+'</a>",'
            data += 'text: "' + file_name + '",'
            data += '},'
        data = data[:-1]
        data += ']'
        data += '},'

    data = data[:-1]
    data += ']'

    return data


# 获取文件内容
def get_bakfile_detail(f_dir_name, c_file_name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_hole_name = dir_name + '/routerbakfile/' + f_dir_name + '/' + c_file_name
    if not os.path.isfile(file_hole_name):
        return False

    with open(file_hole_name) as f:
        bakfiledetail = f.read()

    return bakfiledetail


# 获取文件编码
def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
