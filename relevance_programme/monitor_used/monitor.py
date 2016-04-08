#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import paramiko
import os
from Tools.DBtools import MysqlDb
from Tools.global_function import read_ini, tuple_to_list, write_file, decrypt
from Tools.global_class import Server
from Tools import global_value

dir_name = os.path.dirname(os.path.abspath(__file__))


class Attribute(object):
    def __init__(self, parameter_name, command, table_name, table_column, column_type, type_value, show_type):
        self.parameter_name = parameter_name
        self.command = command
        self.table_name = table_name
        self.table_column = str(table_column).split('/')
        self.column_type = str(column_type).split('/')
        self.type_value = str(type_value).split('/')


class RunShell(object):
    def __init__(self, server):
        self.server = server

    def get_connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.server.ip, int(self.server.port), self.server.user,
                        decrypt(global_value.ENCRYPT_KEY_VALUE, self.server.password))
        except Exception as e:
            write_file(dir_name + "err_log.log", str(e), 'a+')
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

            re_list = [self.server.ip, statu, string_in, string_out, string_err]
            ssh.close()
            return re_list
        else:
            return ssh


def create_table(attribute):
    if check_table_columns(attribute.table_column, attribute.column_type, attribute.type_value):
        c_table_sql = "create table " + attribute.table_name
        c_table_sql += " ( "
        c_table_sql_list = []
        for index, table_column in enumerate(attribute.table_column):
            s = ""
            s += table_column + " " + attribute.column_type[index]
            if attribute.type_value[index] != "null":
                s += " (" + attribute.type_value[index] + ")"
            s += " not null"
            c_table_sql_list.append(s)
        c_table_sql += ",".join(c_table_sql_list)
        c_table_sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
        return c_table_sql


def check_table_columns(table_column_list, column_type_list, type_value_list):
    if len(table_column_list) != len(column_type_list) and len(column_type_list) != len(type_value_list) and len(
            table_column_list) != len(type_value_list):
        return False
    else:
        return True


def get_sql(attribute):
    sql = "INSERT INTO " + attribute.table_name + "("
    sql += ",".join(attribute.table_column)
    sql += ") VALUES ("
    s_list = []
    for i in range(0, len(attribute.table_column)):
        s_list.append("%s")
    sql += ",".join(s_list)
    sql += ")"
    return sql


def get_list(li):
    l = []
    for i in li:
        for b in i:
            l.append(b)
    return l


if __name__ == '__main__':
    # 获取mysql连接
    mysql = MysqlDb('mysql-host')
    # 获取文件路径
    dir_name = os.path.dirname(os.path.abspath(__file__))
    commands_ini = dir_name + '/commands.ini'
    # 读取文件，生成dict
    commands_di = read_ini(commands_ini)
    # 生成attribute类dict
    attribute_di = {}
    attribute_se_list = []
    for se, di in commands_di.items():
        attribute_se_list.append(di['table_name'])
        attribute_di[se] = Attribute(se, di['command'], di['table_name'],
                                     di['table_column'], di['column_type'],
                                     di['type_value'], di['show_type'])

    # 检验数据库是否存在此参数表
    sql = "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'minxinyunwei'"
    rs_tuple = mysql.run_sql(sql)
    rs_list = get_list(tuple_to_list(rs_tuple))
    for table_name in attribute_se_list:
        if table_name not in rs_list:
            # 创建表
            for se, attribute in attribute_di.items():
                if attribute.table_name == table_name:
                    sql = create_table(attribute)
                    rs_tuple = mysql.run_sql(sql)

    # linux 服务器参数抽取
    # 获取待抽取服务器列表
    # sql = "select * from server_list where state = 1"
    sql = "SELECT * FROM server_list_old WHERE ip='192.168.9.155'"
    rs_tuple = mysql.run_sql(sql)
    rs_list = tuple_to_list(rs_tuple)
    server_list = []
    for li in rs_list:
        server = Server(li)
        server.binding_server_value()
        server_list.append(server)

    server_run_shell = {}
    re_run_shell_list = []

    for server in server_list:
        server_run_shell[server.ip] = RunShell(server)

    # 执行shell命令
    for ip, runshell in server_run_shell.items():
        for se, attribute in attribute_di.items():
            re_run_shell_list.append(runshell.run_commands(attribute.command, attribute.parameter_name))

    for li in re_run_shell_list:
        sql_value_list = []
        if li is False:
            continue

        attribute = attribute_di[li[1]]
        if not check_table_columns(attribute.table_column, attribute.column_type, attribute.type_value):
            continue

        # 加载数据处理文件，
        # 文件同一函数名称 data_execute
        # 传入shell返回数据[服务器IP, 数据类型, 返回输入参数, shell返回值, 返回错误信息] 返回类型list
        # 文件名与table_name同名
        fun = None
        try:
            exec ("import " + attribute.table_name)
            exec ("fun = " + attribute.table_name + ".data_execute")
            sql_value_list = fun(li)
        except Exception as e:
            print e
            continue

        sql = get_sql(attribute)
        for i in sql_value_list:
            if isinstance(i,list):
                mysql.run_sql(sql, i)
            else:
                mysql.run_sql(sql, sql_value_list)
