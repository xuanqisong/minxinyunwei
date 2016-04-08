#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import paramiko
import ConfigParser
import time
import os

dir_name = os.path.dirname(os.path.abspath(__file__))


class Server(object):
    def __init__(self, ip, user, password, port, detail):
        self.__ip = ip
        self.__user = user
        self.__password = password
        self.__port = port
        self.__detail = detail

    def get_ip(self):
        return self.__ip

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def get_port(self):
        return self.__port

    def get_disk_name(self):
        return self.__detail


class MysqlDb(object):
    def __init__(self):
        pass

    def get_connect(self):
        #conn = MySQLdb.Connect(host='192.168.9.231', port=3306, user='root', passwd='root', db='minxinyunwei',charset='utf8')
        conn = MySQLdb.Connect(host='10.255.12.233', port=6337, user='root', passwd='root', db='minxinyunwei',charset='utf8')
        return conn

    def run_sql(self, sql, value_li):
        try:
            conn = self.get_connect()
            cu = conn.cursor()
            if value_li <> '':
                cu.execute(sql, value_li)
            else:
                cu.execute(sql)
            rs = cu.fetchall()
            cu.close
            conn.commit()
            return rs
        except Exception as e:
            print "Mysql error:", e
            cu.close()
            conn.rollback()
            return False
        finally:
            conn.close


class Run_Shell(object):
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

    def get_connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip, int(self.port), self.user, self.password)
        except Exception as e:
            write_file(dir_name+"err_log.log",e,'a')
            return False
        return ssh

    def run_commands(self, commands, statu):
        string_in = ''
        string_err = ''
        ssh = self.get_connect()
        if ssh:
            stdin, stdou, stderr = ssh.exec_command(commands)
            try:
                for i in stdin.readlines():
                    string_in += i.replace("\n", "")
            except Exception as e:
                pass
            try:
                if statu == "disk":
                    string_out = []
                    string_out = stdou.readlines()
                else:
                    string_out = ""
                    for i in stdou.readlines():
                        string_out += i.replace("\n", "")
            except Exception as e:
                pass
            try:
                for i in stderr.readlines():
                    string_err += i.replace("\n", "")
            except Exception as e:
                pass
            re_string = [self.ip, statu, string_in, string_out, string_err]
            ssh.close()
            return re_string
        else:
            return ssh



def write_file(filepath, txt, method):
    try:
        f = open(filepath, method)
        txt_type = str(type(txt))[7:12]
        if txt_type == 'tuple':
            for va in txt:
                f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(va))
                f.write(' ')
        elif txt_type == 'list':
            for va in txt:
                f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(va))
                f.write(' ')
        elif txt_type == 'dict':
            for va in txt.iteritems():
                f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(va[0]))
                f.write(':')
                f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(va[1]))
                f.write(' ')
        else:
            f.write("[log:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "]" + str(txt))
            f.write(' ')
        f.write('\n')
        f.close
    except Exception as e:
        print "write file error :", txt
        print "file path :", filepath
        print "error message :", e
        exit()


def read_ini(path, target):
    cfp = ConfigParser.ConfigParser()
    cfp.read(path)
    di = {}
    for se in cfp.sections():
        if se == target:
            for va in cfp.items(se):
                di[va[0]] = va[1]
    return di


def tuple_to_list(tu):
    li = []
    for va1 in tu:
        type_va1 = str(type(va1))[7:12]
        if type_va1 == 'tuple':
            li.append(tuple_to_list(va1))
        else:
            li.append(change_utf8(va1))
    return li


def change_utf8(string):
    try:
        txt = str(string).encode("utf-8")
    except Exception as e:
        txt = string
    return txt

if __name__ == '__main__':

    mysql = MysqlDb()
    dir_name = os.path.dirname(os.path.abspath(__file__))
    commands_ini = dir_name + '/commands.ini'
    commands_di = read_ini(commands_ini, 'command')
    server_list = []
    server_run_shell = {}
    re_run_shell_list = []

    rs_tuple = mysql.run_sql("select * from server_list where state = 1", '')
    rs_list = tuple_to_list(rs_tuple)

    for li in rs_list:
        server_list.append(Server(li[0], li[1], li[2], li[3], li[4]))

    for server in server_list:
        server_run_shell[server.get_ip()] = Run_Shell(server.get_ip(), int(server.get_port()), server.get_user(),
                                                      server.get_password())

    for k, v in server_run_shell.items():
        for a, b in commands_di.items():
            re_run_shell_list.append(v.run_commands(b, a))

    for li in re_run_shell_list:
        sql_value_list = []
        if li is False:
            continue
        elif li[1] == 'cpu':
            sql = "insert into statu_cpu (ip,time,used) values (%s,%s,%s)"
            sql_value_list.append(li[0])
            sql_value_list.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            a = float(li[3][:-4])
            used = ("%.2f" % a)
            sql_value_list.append(used)
            mysql.run_sql(sql, sql_value_list)

        elif li[1] == 'mem':
            sql = "insert into statu_memory (ip,time,total,free,busy,used) values (%s,%s,%s,%s,%s,%s)"
            re_string_list = li[3].split("#")
            total = int(re_string_list[0])
            # use = int(re_string_list[1])
            free = int(re_string_list[2])
            cached = int(re_string_list[3])
            use = total - free - cached
            a = (float(use) / float(total)) * 100
            used = ("%.2f" % a)

            sql_value_list.append(li[0])
            sql_value_list.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            sql_value_list.append(total)
            sql_value_list.append(use)
            sql_value_list.append(free)
            sql_value_list.append(used)

            mysql.run_sql(sql, sql_value_list)

        elif li[1] == 'disk':
            sql = "insert into statu_disk (ip,time,total,free,busy,used,disk_name) values (%s,%s,%s,%s,%s,%s,%s)"

            disk_rs_list = li[3]
            for k in range(0, len(disk_rs_list)):
                sql_value_list = []
                if k != 0:
                    re_string_list = disk_rs_list[k].split("#")

                    # re_string_list = li[3].split("#")
                    total = int(re_string_list[0])
                    use = int(re_string_list[1])
                    free = int(re_string_list[2])
                    # a = (float(use) / float(total)) * 100
                    used = int(re_string_list[3].replace("%", ""))
                    disk_name = re_string_list[4].replace("\n", "")

                    sql_value_list.append(li[0])
                    sql_value_list.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                    sql_value_list.append(total)
                    sql_value_list.append(free)
                    sql_value_list.append(use)
                    sql_value_list.append(used)
                    sql_value_list.append(disk_name)

                    mysql.run_sql(sql, sql_value_list)
