# -*- coding: utf-8 -*-
import hashlib
import os
import time
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
    sql = "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'minxinyunwei' AND table_name like 'status%'"
    re_tu = mysql.run_sql(sql)
    return re_tu


# file manager
def get_file_detail(request):
    # 文件夹列表
    dir_set = global_value.HOME_FILE_SHOW_PERMISSIONS
    # 获取用户
    u = request.user
    # 获取用户所有权限
    p = u.get_all_permissions()
    # # 权限列表
    # p_list = global_value.HOME_FILE_MANAGER_PERMISSIONS
    # 此文件的文件夹名称
    path = os.path.dirname(__file__)
    # 文件总目录
    file_manager_path = os.path.dirname(path) + "/servicefilemanager"
    # 展示权限列表
    show_dir_p = ([])
    for d in dir_set:
        dd = "home.home_" + d + "_show"
        if dd in p:
            show_dir_p.append(d)

    data_li = []
    for d in show_dir_p:
        string = "{"
        d_name = global_value.HOME_FILE_SHOW_DICT[d]
        string += 'text: "' + d_name + '"'
        re_string = get_tree_date(file_manager_path + "/" + d)
        if len(re_string) > 0:
            string += ", selectable: false,"
            string += "nodes: [" + re_string + "]"
        string += "}"
        data_li.append(string)

    return ",".join(data_li)


# 获取文件展示list p_name是文件路径 dir_path_list是文件路径的列表dir_path_list = os.path.listdir(p_name)
def get_tree_date(p_name, dir_path_list=None):
    if dir_path_list is None:
        if os.path.exists(p_name):
            dir_path_list = os.listdir(p_name)
        else:
            return "{ text: no file}"
    str_list = []
    if len(dir_path_list) == 0:
        string = '{'
        string += 'text: "' + str(p_name).split("/")[-1] + '"'
        string += '}'
        str_list.append(string)
    else:
        for dirorfilename in dir_path_list:
            string = '{'
            string += 'text: "' + dirorfilename + '"'
            if os.path.isdir(p_name + "/" + dirorfilename):
                string += ',selectable: false ,'
                string += 'nodes:'
                string += '['

                string += get_tree_date(p_name + "/" + dirorfilename, os.listdir(p_name + "/" + dirorfilename))

                string += ']'
                string += '}'
            else:
                string += '}'
            str_list.append(string)
    return ",".join(str_list)


def get_dir_list(file_path):
    di = {}
    if os.path.isdir(file_path):
        for ob in os.listdir(file_path):
            di.update(get_dir_list(file_path + "/" + ob))

    else:
        di[str(file_path).split('/')[-1]] = file_path
    return di


# 获取文件属性
def file_attribute(file_name):
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_name_file_path_di = get_dir_list(base_path + "/servicefilemanager")
    file_path = file_name_file_path_di[file_name]

    file_detail = os.stat(file_path)
    # create time
    file_create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_detail.st_ctime))
    # change time
    file_change_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_detail.st_mtime))

    # MD5
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        m.update(f.read())

    file_md5 = m.hexdigest()
    di = {'file_name': file_name, 'file_size': file_detail.st_size, 'file_create_time': file_create_time,
          'file_change_time': file_change_time, 'file_md5': file_md5}

    return di


# 获取用户上传下载权限
def user_permissions(request):
    # 获取用户
    u = request.user
    # 获取用户所有权限
    p = u.get_all_permissions()
    permissions_list = ['home.home_file_download', 'home.home_file_upload']
    re_per = {"u_p": []}
    for li in permissions_list:
        if li in p:
            re_per["u_p"].append(li)

    return re_per


# uploadfile and save file in localpath
def save_file(request):
    try:
        path = os.path.dirname(os.path.dirname(__file__))
        user = request.user
        dir_file = path + "/servicefilemanager/uploadfiledir/"
        dir_exists_or_create(dir_file)

        # dir_file += str(user) + "/"
        ymr = time.strftime("%Y%m%d", time.localtime(time.time()))
        dir_file += ymr + "/"

        dir_exists_or_create(dir_file)

        ymrhms = time.strftime("%Y%m%d%H", time.localtime(time.time()))
        dir_file += ymrhms + "/"

        dir_exists_or_create(dir_file)
        dir_exists_or_create(dir_file + "sqlscript")
        dir_exists_or_create(dir_file + "softfile")

        # 获取文件名称
        web_f = request.FILES['upfile']
        f_type = str(web_f).split('.')[-1]

        if f_type == 'txt' or f_type == 'sql':
            dir_file += "sqlscript/"
        else:
            dir_file += "softfile/"

        file_name = web_f.name
        f = open(dir_file + file_name, 'wb+')
        for chunk in web_f.chunks():
            f.write(chunk)
        f.close()
        return True
    except Exception as e:
        print e
        return False


# yield file
def download_file(request):
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_name_file_path_di = get_dir_list(base_path + "/servicefilemanager")

    file_name = request.POST.get('file_name')
    path = file_name_file_path_di[file_name]
    # 获取文件迭代
    yield_bit = file_iterator(path)
    return yield_bit


# 检查文件夹是否存在，不存在则创建
def dir_exists_or_create(file_dir):
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)


# 文件迭代
def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
