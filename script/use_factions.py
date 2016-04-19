# -*- coding: utf-8 -*-
from Tools import global_function
from Tools.DBtools import MysqlDb

from script.baseclass import *
import paramiko, os, time

from Tools import global_value

import hashlib


# def get_serverlist():
#     sql_server_list = "select * from server_list WHERE servertype='3'"
#     mysql = MysqlDb('mysql-host')
#     rs_tu = mysql.run_sql(sql_server_list, '')
#     rs_li = global_function.tuple_to_list(rs_tu)
#     servernamelist = []
#     for li in rs_li:
#         a = Serverlist(li[0], li[1], li[2], li[3], li[4])
#         servernamelist.append(a)
#     return servernamelist


# 获取服务器，组别列表
def get_server_grouplist():
    re_li = []
    sql = "SELECT DISTINCT(`group`) FROM server_list WHERE  servertype='3'"

    mysql = MysqlDb('mysql-host')
    rs_tu = mysql.run_sql(sql, '')
    for tu in rs_tu:
        re_li.append(tu[0])
    return re_li


# # 服务器增删改查
# # 检验服务器字段
# def check_server_field(request, method):
#     # 检验重复IP
#     server_list = get_serverlist()
#     server_iplist = []
#     for old_server in server_list:
#         server_iplist.append(old_server.get_ip())
#     # 校对字段
#     check_report = {'report': True}
#     if method == "new":
#         server_ip1 = request.POST.get('server_ip1')
#         server_ip2 = request.POST.get('server_ip2')
#         server_ip3 = request.POST.get('server_ip3')
#         server_ip4 = request.POST.get('server_ip4')
#
#         server_ip = str(server_ip1) + "." + str(server_ip2) + "." + str(server_ip3) + "." + str(server_ip4)
#     else:
#         server_ip = request.POST.get('server_ip')
#
#     if request.POST.get('server_detail') == '':
#         server_detail = server_ip
#     else:
#         server_detail = request.POST.get('server_detail')
#
#     if request.POST.get('server_group') == '':
#         server_group = 'test'
#     else:
#         server_group = request.POST.get('server_group')
#     # 对密码进行加密
#     encrypt_pas = global_function.encrypt(global_value.ENCRYPT_KEY_VALUE, request.POST.get('server_password'))
#     # server = Server(server_ip, request.POST.get('server_user'), request.POST.get('server_password'),
#     #                 request.POST.get('server_port'), server_detail,
#     #                 server_group, request.POST.get('server_state'))
#     server = Server(server_ip, request.POST.get('server_user'), encrypt_pas,
#                     request.POST.get('server_port'), server_detail,
#                     server_group, request.POST.get('server_state'))
#     # check ip
#     if method == "new":
#         if server_ip in server_iplist:
#             check_report['server_ip'] = "此服务器已存在"
#             check_report['report'] = False
#
#         if server_ip1 == '' or server_ip2 == '' or server_ip3 == '' or server_ip4 == '':
#             check_report['server_ip'] = "IP不可为空"
#             check_report['report'] = False
#
#     # check_server_user
#     if server.get_user() == '':
#         check_report['server_user'] = "服务器用户名不可为空"
#         check_report['report'] = False
#
#     # check_server_user
#     if method == "change":
#         if not check_old_password(server_ip, request.POST.get('server_password_o')):
#             check_report['server_password_o'] = "旧服务密码输入错误"
#             check_report['report'] = False
#
#     if server.get_password() == '':
#         check_report['server_password'] = "密码不能为空"
#         check_report['report'] = False
#
#     if request.POST.get('server_password_t') != global_function.decrypt(global_value.ENCRYPT_KEY_VALUE,
#                                                                         server.get_password()):
#         check_report['server_password_t'] = "两次输入的密码不同"
#         check_report['report'] = False
#
#     # check_server_port
#     if server.get_port() == '':
#         check_report['server_port'] = "端口号不能为空"
#         check_report['report'] = False
#
#     check_report['server'] = server
#
#     return check_report


# # 插入修改server信息
# def insert_server(server):
#     mysql = MysqlDb('mysql-host')
#     server_list = [server.get_ip(), server.get_user(), server.get_password(), int(server.get_port()),
#                    server.get_detail(),
#                    server.get_group(), int(server.get_state())]
#     value_list = [server.get_user(), server.get_password(), int(server.get_port()), server.get_detail(),
#                   server.get_group(),
#                   int(server.get_state())]
#     sql = "insert into server_list values(%s,%s,%s,%s,%s,%s,%s,'3') on duplicate key update user=%s,password=%s,port=%s,detail=%s,`group`=%s,state=%s,servertype='3'"
#     rs_tu = mysql.run_sql(sql, server_list + value_list)
#     if len(rs_tu) == 0:
#         return True
#     else:
#         return False


# # 删除指定IP，非删除，将IP备份的备份表中
# def delete_bak_server(server_ip_list):
#     mysql = MysqlDb('mysql-host')
#     ip_list = ''
#     for ip in server_ip_list:
#         ip_list = ip_list + "'" + ip + "',"
#     sql = "insert into server_list_bak SELECT *,now() from server_list where ip in (" + ip_list[:-1] + ")"
#     rs_tu = mysql.run_sql(sql, '')
#     if len(rs_tu) == 0:
#         sql = "delete from server_list where ip in (" + ip_list[:-1] + ")"
#         rs_tu = mysql.run_sql(sql, '')
#         if len(rs_tu) == 0:
#             return True
#         else:
#             return False
#     else:
#         return False


# # 修改指定服务器参数
# def read_server(ip):
#     mysql = MysqlDb('mysql-host')
#     sql = "select * from server_list where ip = %s"
#     rs_tu = mysql.run_sql(sql, ip)
#     rs_li = global_function.tuple_to_list(rs_tu)
#     for li in rs_li:
#         server = Server(li[0], li[1], li[2], li[3], li[4], li[5], li[6])
#
#     return server


def check_old_password(ip, pas):
    mysql = MysqlDb('mysql-host')
    sql = "select count(*) from server_list where ip=%s and password=%s"
    rs_tu = mysql.run_sql(sql, [ip, global_function.encrypt(global_value.ENCRYPT_KEY_VALUE, pas)])
    if rs_tu[0][0] > 0:
        return True
    else:
        return False


# def call_procedure(procedure_name, methon, table_name):
#     mysql = MysqlDb('mysql-host')
#     conn = mysql.get_connect()
#     cur = conn.cursor()
#     if methon == 'new':
#         cur.callproc(procedure_name, (table_name,))
#     else:
#         cur.callproc(procedure_name, (table_name,))
#     data = cur.fetchall()
#     return True


# 获取服务器详细信息
def get_group_server_detail(group_name):
    mysql = MysqlDb('mysql-host')
    sql = "SELECT ip,user,detail FROM server_list WHERE `group`=%s"
    rs_tu = mysql.run_sql(sql, group_name)
    rs_li = global_function.tuple_to_list(rs_tu)
    di_group_server_detail = {}
    for li in rs_li:
        di_group_server_detail[li[0]] = [li[1], li[2]]
    return di_group_server_detail


# 获取SSH页面基础信息
def get_websshbase(connect_serverip):
    mysql = MysqlDb('mysql-host')
    class_li = []
    for ip in connect_serverip:
        sql = "SELECT user,password,`group`,port FROM server_list WHERE ip=%s"
        re_tu = mysql.run_sql(sql, ip)
        re_li = global_function.tuple_to_list(re_tu)
        li = re_li[0]
        class_li.append(WebSSHBase(li[0], li[1], ip, ip.replace('.', ''), li[2], '未连接', '', li[3]))
    return {'class_li': class_li}


def get_file_name_list(request):
    path = os.path.dirname(os.path.dirname(__file__))
    user = request.user
    if request == '':
        dir_name = path + "/servicefilemanager/"
    else:
        dir_name = path + "/servicefilemanager/" + str(user) + "/"

    if os.path.isdir(dir_name):
        file_name_list = os.listdir(dir_name)
    else:
        os.mkdir(dir_name)
        file_name_list = os.listdir(dir_name)
    return file_name_list


# def get_downloadfile(request):
#     file_name_list = get_file_name_list(request)
#     data = '['
#     data += '{ '
#     data += 'text: "' + "文件夹" + '",'
#     data += 'selectable: false,'
#     data += 'nodes:['
#     for file_name in file_name_list:
#         data += '{'
#         # data += 'text: "<a href="javascript: clickfile()">'+file_name+'</a>",'
#         data += 'text: "' + file_name + '",'
#         data += '},'
#     data = data[:-1]
#     data += ']'
#     data += '},'
#
#     data = data[:-1]
#     data += ']'
#     return data


# # create time, change time, MD5, file size, file name
# def get_file_detail(file_name, request):
#     path = os.path.dirname(os.path.dirname(__file__))
#     user = request.user
#     dir_file_name = path + "/servicefilemanager/" + str(user) + "/" + file_name
#     file_attribute = os.stat(dir_file_name)
#     # create time
#     file_create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_attribute.st_ctime))
#     # change time
#     file_change_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_attribute.st_mtime))
#
#     # MD5
#     m = hashlib.md5()
#     with open(dir_file_name, 'rb') as f:
#         m.update(f.read())
#
#     file_md5 = m.hexdigest()
#     di = {'file_name': file_name, 'file_size': file_attribute.st_size, 'file_create_time': file_create_time,
#           'file_change_time': file_change_time, 'file_md5': file_md5}
#
#     return di


# # uploadfile and save file in localpath
# def save_file(request):
#     try:
#         path = os.path.dirname(os.path.dirname(__file__))
#         user = request.user
#         dir_file = path + "/servicefilemanager/"
#         if not os.path.exists(dir_file):
#             os.mkdir(dir_file)
#
#         dir_file += str(user) + "/"
#
#         web_f = request.FILES['upfile']
#         file_name = web_f.name
#         f = open(dir_file + file_name, 'wb+')
#         for chunk in web_f.chunks():
#             f.write(chunk)
#         f.close()
#         return True
#     except Exception as e:
#         print e
#         return False


# # servicefilemanager
# def downloadfile(request):
#     path = os.path.dirname(os.path.dirname(__file__))
#     file_name = request.POST.get('file_name')
#     # 获取文件迭代
#     user = request.user
#     yield_bit = file_iterator(path + "/servicefilemanager/" + str(user) + "/" + file_name)
#     return yield_bit
#
#
# # gei file yield
# def file_iterator(file_name, chunk_size=512):
#     with open(file_name) as f:
#         while True:
#             c = f.read(chunk_size)
#             if c:
#                 yield c
#             else:
#                 break


# monitor = Monitor()
# paramiko 容器
# paramiko_rec_di = {}
# paramiko_send_di = {}
# paramiko_file_sendreceive_di = {}
# prun_di = {}
# server_ip_list = []

monitor_random_id_di = {}
client_random_id = {}


def analyze_head_messages(messages):
    return str(messages).split('/')


def clients_ids(clients):
    di = {}
    for client in clients:
        di[id(client)] = client
    return di


def add_client_random_id(html_random_id, clients_di):
    client_id_list = []
    for r_id, c_id in client_random_id.items():
        if c_id not in client_id_list:
            client_id_list.append(c_id)

    for client_id, client in clients_di.items():
        if html_random_id not in client_random_id:
            if client_id not in client_id_list:
                client_random_id[html_random_id] = client_id


# 检测message
def detection_message(messages, web_ssh_server_list, clients):
    try:
        message_di = json.loads(messages)
        message = ""
        html_random_id = ""
        clients_di = ""
    except Exception:
        message, html_random_id = analyze_head_messages(messages)
        clients_di = clients_ids(clients)
        # for client_id, client in clients_di.items():
        #     if html_random_id not in client_random_id:
        #         client_random_id[html_random_id] = client_id
        add_client_random_id(html_random_id, clients_di)
        message_di = ""

    if message == 'thread':
        new_or_old_thread(web_ssh_server_list, clients_di[client_random_id[html_random_id]], html_random_id)
    elif message == 'start':
        start_connect(html_random_id)
    elif message == 'shutdown':
        stop_thread(html_random_id)
    elif message == 'disconnect':
        disconnect_all_thread(html_random_id)
    else:
        # 解析json字符串
        # 页面回传格式,第一种：{single:{commander:'shutdown/send/uploadfile/servicefilemanager',commandertext:'',ip:''}},第二种：{all:{commander:'send/uploadfile/servicefilemanager',commandertext:''}}
        # message_di = json.loads(messages)
        if not isinstance(message_di, dict):
            print message_di
            return

        analyze_message(message_di, clients)
    return web_ssh_server_list


def analyze_message(message_di, clients):
    for sys_coms, com_di in message_di.items():
        # 单服务器模式

        sys_com, html_random_id = analyze_head_messages(sys_coms)
        monitor = monitor_random_id_di[html_random_id]

        if sys_com == 'single':

            if com_di['commander'] == 'send':
                # paramiko_send_di[com_di['ip']].send_text = com_di['commandertext']
                monitor.thread_p_send[com_di['ip']].send_text = com_di['commandertext']
            elif com_di['commander'] == 'disconnect':
                # prun_di[com_di['ip']].close_channel()
                # prun_di[com_di['ip']].close_sftp()
                # prun_di[com_di['ip']].close_ssh()
                monitor.prun[com_di['ip']].close_channel()
                monitor.prun[com_di['ip']].close_sftp()
                monitor.prun[com_di['ip']].close_ssh()

            elif com_di['commander'] == 'uploadfile':
                upload_download_file(com_di['ip'], com_di['localpath'], com_di['remotepath'], clients, com_di['user'],
                                     'send', html_random_id)
            elif com_di['commander'] == 'servicefilemanager':
                upload_download_file(com_di['ip'], com_di['localpath'], com_di['remotepath'], clients, com_di['user'],
                                     'receive', html_random_id)

        elif sys_com == 'all':
            if com_di['commander'] == 'send':
                # for ip, p_send in paramiko_send_di.items():
                for ip, p_send in monitor.thread_p_send.items():
                    p_send.send_text = com_di['commandertext']
            elif com_di['commander'] == 'uploadfile':
                upload_download_file(None, com_di['localpath'], com_di['remotepath'], clients, com_di['user'], 'send',
                                     html_random_id)
            elif com_di['commander'] == 'servicefilemanager':
                upload_download_file(None, com_di['localpath'], com_di['remotepath'], clients, com_di['user'],
                                     'receive', html_random_id)

        else:
            return


def new_or_old_thread(web_ssh_server_list, client, html_random_id):
    if html_random_id not in monitor_random_id_di:
        new_and_start_thread(web_ssh_server_list, client, html_random_id)
    else:
        start_connect(html_random_id)
        pass


# def old_and_start_child_thread(html_random_id):
#     monitor = monitor_random_id_di[html_random_id]
#     for ip, prun in monitor.prun.items():
#         if not prun.ssh[0]:
#             prun.get_connect_ssh()
#             prun.get_connect_channel()
#             prun.get_connect_sftp()


def new_and_start_thread(web_ssh_server_list, client, html_random_id):
    monitor = Monitor()
    # 监控线程
    monitor.client = client
    prun_di = {}
    paramiko_rec_di = {}
    paramiko_send_di = {}
    paramiko_file_sendreceive_di = {}
    server_ip_list = []

    monitor.prun = prun_di
    monitor.thread_p_rec = paramiko_rec_di
    monitor.thread_p_send = paramiko_send_di
    monitor.thread_file_send_receive = paramiko_file_sendreceive_di
    monitor.server_ip_list = server_ip_list

    for websshbase in web_ssh_server_list:
        prun = PRun(websshbase.get_ip(), websshbase.get_port(), websshbase.get_user(), websshbase.get_pas())
        prun_di[websshbase.get_ip()] = prun

    for ip, prun in prun_di.items():
        paramiko_rec_di[ip] = PRec(ip, prun)
        paramiko_send_di[ip] = PSend(ip, prun)
        paramiko_file_sendreceive_di[ip] = FileSendReceive(ip, prun)

    for websshbase in web_ssh_server_list:
        server_ip_list.append(websshbase.get_ip())

    for ip, p_rec in paramiko_rec_di.items():
        if not p_rec.is_alive():
            p_rec.start()
    for ip, p_send in paramiko_send_di.items():
        if not p_send.is_alive():
            p_send.start()
    for ip, file_send_receive in paramiko_file_sendreceive_di.items():
        if not file_send_receive.is_alive():
            file_send_receive.start()

    monitor.start()
    monitor_random_id_di[html_random_id] = monitor


def upload_download_file(ip, local_path, remote_path, clients, user, file_type, html_random_id):
    send_str = {'alert': ''}
    path = os.path.dirname(os.path.dirname(__file__))
    lo_path = path + "/servicefilemanager/" + user + "/" + local_path

    monitor = monitor_random_id_di[html_random_id]
    if not monitor.is_alive():
        return

    if ip is None:
        # for ip_name, file_send_receive in paramiko_file_sendreceive_di.items():
        for ip_name, file_send_receive in monitor.thread_file_send_receive.items():
            if not file_send_receive.start_t:
                if file_type == 'receive':
                    lo_path = path + "/servicefilemanager/" + user + "/" + str(ip_name).replace('.', '') + local_path
                file_send_receive.local_path = lo_path
                file_send_receive.remote_path = remote_path
                file_send_receive.file_type = file_type
                file_send_receive.start_t = True
            else:
                send_str['alert'] += "<" + ip_name + "> is" + file_send_receive.file_type + "ing File <br/>"
    else:
        # if not paramiko_file_sendreceive_di[ip].start_t:
        if not monitor.thread_file_send_receive[ip].start_t:
            if file_type == 'receive':
                lo_path = path + "/servicefilemanager/" + user + "/" + str(ip).replace('.', '') + local_path
            monitor.thread_file_send_receive[ip].local_path = lo_path
            monitor.thread_file_send_receive[ip].remote_path = remote_path
            monitor.thread_file_send_receive[ip].file_type = file_type
            monitor.thread_file_send_receive[ip].start_t = True
        else:
            send_str['alert'] += "<" + ip + "> is " + monitor.thread_file_send_receive[ip].file_type + "ing File <br/>"

    if send_str['alert'] != '':
        send_json = json.dumps(send_str)
        for client in clients:
            client.send(send_json)


def stop_thread(html_random_id):
    # monitor = Monitor()
    # if len(clients) < 2:
    #     monitor.monitor = False
    #     monitor.join()
    #     paramiko_file_sendreceive_di.clear()
    #     paramiko_send_di.clear()
    #     paramiko_rec_di.clear()
    #     while monitor.is_alive():
    #         print "monitor is alive"
    #     del monitor
    try:
        monitor = monitor_random_id_di[html_random_id]
        monitor.monitor = False
        monitor.join()

        del monitor_random_id_di[html_random_id]
        # del client_di[client_random_id[client_random_id]]
        del client_random_id[html_random_id]
    except Exception as e:
        print e


def disconnect_all_thread(html_random_id):
    # for ip, p_run in prun_di.items():
    #     p_run.close_channel()
    #     p_run.close_sftp()
    #     p_run.close_ssh()
    monitor = monitor_random_id_di[html_random_id]
    for ip, prun in monitor.prun.items():
        prun.close_channel()
        prun.close_sftp()
        prun.close_ssh()


def start_connect(html_random_id):
    monitor = monitor_random_id_di[html_random_id]
    for ip, p_run in monitor.prun.items():
        if not p_run.ssh[0]:
            p_run.get_connect_ssh()
            p_run.get_connect_channel()
            p_run.get_connect_sftp()
