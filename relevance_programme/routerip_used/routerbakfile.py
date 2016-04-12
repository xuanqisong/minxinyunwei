# -*- coding: utf-8 -*-

import time
import paramiko
import os
import MySQLdb


class Server(object):
    def __init__(self, sql_list):
        self.sql_list = sql_list
        self.ip = ''
        self.user = ''
        self.password = ''
        self.port = ''
        self.detail = ''
        self.group = ''
        self.statu = ''
        self.servertype = ''
        self.monitor_value = ''

    def binding_server_value(self):
        self.ip = self.sql_list[0]
        self.user = self.sql_list[1]
        self.password = self.sql_list[2]
        self.port = self.sql_list[3]
        self.detail = self.sql_list[4]
        self.group = self.sql_list[5]
        self.statu = self.sql_list[6]
        self.servertype = self.sql_list[7]
        # self.monitor_value = self.sql_list[8]


class MysqlDb(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def get_connect(self):
        self.conn = MySQLdb.Connect(host='10.255.12.233', port=int(6337), user='root', passwd='root', db='minxinyunwei',
                                    charset='utf8')

    def run_sql(self, sql, value_li=''):
        try:
            self.get_connect()
            try:
                cu = self.conn.cursor()
                if value_li != "":
                    cu.execute(sql, value_li)
                else:
                    cu.execute(sql)

                rs = cu.fetchall()
                self.conn.commit()
                cu.close()
                self.conn.close()
                return rs

            except Exception as e:
                self.conn.rollback()
                self.conn.close()
                return False

        except Exception as e:
            return False

    def run_uid(self, sql, value_li=''):
        try:
            self.get_connect()
            try:
                cu = self.conn.cursor()
                if value_li != "":
                    cu.execute(sql, value_li)
                else:
                    cu.execute(sql)

                count = cu.rowcount
                self.conn.commit()
                cu.close()
                self.conn.close()
                return count

            except Exception as e:
                self.conn.rollback()
                self.conn.close()
                return False

        except Exception as e:
            return False


class ParamikoRun(object):
    def __init__(self, server):
        self.server = server

    def getsshconnect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.server.ip, int(self.server.port), self.server.user,
                    self.server.password)
        return ssh


# 转码函数
def change_utf8(string):
    try:
        txt = str(string).encode("utf-8")
    except Exception:
        txt = string
    return txt


def tuple_to_list(tu):
    li = []
    for va1 in tu:
        if isinstance(va1, tuple):
            li.append(tuple_to_list(va1))
        else:
            li.append(change_utf8(va1))
    return li


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


if __name__ == "__main__":
    mysql = MysqlDb('mysql-host')
    sql = "SELECT * FROM server_list WHERE servertype='2'"
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
        re_buff += channel.recv(2048)
        # while re_buff.endswith('---- More ----'):
        while True:
            if not re_buff.endswith('---- More ----'):
                if re_buff.endswith('>'):
                    break
            channel.send(''' ''')
            time.sleep(3)
            re_buff += channel.recv(2048)
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
