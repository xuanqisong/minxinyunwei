# -*- coding: utf-8 -*-

import time
import paramiko
import os
from Tools.global_function import write_file, decrypt, tuple_to_list
from Tools.DBtools import MysqlDb
from Tools import global_value
from Tools.global_class import Server


class ParamikoRun(object):
    def __init__(self, server):
        self.server = server

    def getsshconnect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.server.ip, int(self.server.port), self.server.user,
                    self.server.password)
        return ssh


if __name__ == "__main__":
    mysql = MysqlDb('mysql-host')
    sql = "SELECT * FROM server_list_old WHERE ip='10.255.254.131'"
    rs_tuple = mysql.run_sql(sql)
    rs_list = tuple_to_list(rs_tuple)
    server_list = []
    for li in rs_list:
        server = Server(li)
        server.binding_server_value()
        server_list.append(server)
    # user = 'xuanqisong'
    # password = 'xuanqisong@123'
    # ip_father_list = ['10.10.15.126', '10.10.15.124', '10.10.15.125']
    # ip_father_list = ['10.10.15.126']
    paramikodi = {}
    ip_file = {}
    for server in server_list:
        paramikodi[server.ip] = ParamikoRun(server)

    for ip, paramikorun in paramikodi.items():
        ssh = paramikorun.getsshconnect()
        channel = ssh.invoke_shell()
        # 输入指令
        channel.send('''display current-configuration \n''')
        # 等待命令返回
        time.sleep(1)
        re_buff = ''
        re_buff += channel.recv(9999)
        while re_buff.endswith('---- More ----'):
            channel.send(''' ''')
            time.sleep(1)
            re_buff += channel.recv(9999)
        # # 清理无用字符
        re_buff = re_buff.replace('  ---- More ----\x1b[42D                                          \x1b[42D', '')
        ip_file[ip] = re_buff

    # 获取文件名
    dir_name = os.path.dirname(os.path.abspath(__file__))
    time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 文件本身路径(出去文件名称)
    dir_name = os.path.dirname(os.path.abspath(__file__))
    # 获取文件上层目录
    dir_name_up = os.path.abspath(os.path.join(dir_name, os.path.pardir))
    # 获取文件上层目录
    dir_name_upup = os.path.abspath(os.path.join(dir_name_up, os.path.pardir))

    dir_name = dir_name_upup + '/servermanager/routerbakfile'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    dir_name = dir_name + '/' + time_now
    os.mkdir(dir_name)
    ip_file_name = {}
    for ip in paramikodi:
        ip_file_name[ip] = dir_name + '/' + ip.replace('.', '') + '_configuration.txt'

    # 写文件
    for ip, file_name in ip_file_name.items():
        txt = ip_file[ip]
        write_file(file_name, txt, 'w')
