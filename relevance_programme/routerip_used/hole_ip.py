# -*- coding: utf-8 -*-
import MySQLdb
import time
import paramiko



class MySql(object):
    def __init__(self, host, port, user, passwd, db, charset):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset

    def get_connect(self):
        conn = MySQLdb.Connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                               charset=self.charset)
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
            # conn.close()
            return rs
        except Exception as e:
            print e
            cu.close()
            conn.rollback()
            conn.close()
            return False


class ParamikoRun(object):
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

    def runcommand(self, commanders):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, int(self.port), self.user, self.password)
        stdin, stdout, stderr = ssh.exec_command(commanders)
        stdout_str = stdout.readlines()
        ssh.close()
        return stdout_str

    def getsshconnect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, int(self.port), self.user, self.password)
        return ssh


def handle_re_strrange(stdout, ip):
    re_li = []
    if ip == '10.10.15.126':
        for a in stdout:
            i = str(a).replace('\r\n', '')
            if str(i)[:6] == 'Vlanif':
                li = []
                for o in str(i).split(' '):
                    if o == '':
                        pass
                    else:
                        li.append(o)
                if li[1] <> 'unassigned':
                    re_li.append(li[1])
    else:
        for a in stdout:
            i = str(a).replace('\r\n', '')
            if str(i)[:4] == 'Vlan':
                li = []
                for o in str(i).split(' '):
                    if o == '':
                        pass
                    else:
                        li.append(o)
                if li[3] <> 'unassigned':
                    re_li.append(li[3])

    return re_li


def handle_re_strip(stdout, ip):
    re_li = []
    if ip == '10.10.15.126':
        value_s_l = []
        for index, value in enumerate(stdout):
            if value[0:1] == '-':
                value_s_l.append(index)
        if (int(value_s_l[1]) - int(value_s_l[0])) > 1:
            for index in range(value_s_l[0] + 1, value_s_l[1]):
                re_li.append(stdout[index])
    else:
        for index in range(10, len(stdout) - 1):
            re_li.append(stdout[index])

    return re_li


def get_ip_mac_port(str_list, ip):
    re_li = []
    if ip == '10.10.15.126':
        for l1 in str_list:
            li = []
            for l2 in str(l1).split(' '):
                if l2 <> '':
                    if l2 == '1':
                        continue
                    li.append(l2)

            if len(li)==5:
                re_li.append([li[0], li[1], li[4]])
            elif len(li)==4:
                re_li.append([li[0], li[1], li[3]])
    else:
        for l1 in str_list:
            li = []
            for l2 in str(l1).split(' '):
                if l2 <> '':
                    li.append(l2)
            re_li.append([li[0], li[1], li[3]])
    return re_li


if __name__ == "__main__":
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    user = 'xuanqisong'
    passowrd = 'xuanqisong@123'
    ip_father_list = ['10.10.15.126', '10.10.15.124', '10.10.15.125']
    # ip_father_list = ['10.10.15.126']
    paramikodi = {}
    # 获取网关交换机arp表
    # 获取网关交换机连接
    ip_range_di = {}
    for ip in ip_father_list:
        paramikodi[ip] = ParamikoRun(ip, 22, user, passowrd)
    # 获取网关交换机全文
    server_holeip = {}
    for ip, paramikorun in paramikodi.items():
        ssh = paramikorun.getsshconnect()
        # 获取交互式长连接
        channel = ssh.invoke_shell()
        # 开始获取IP全文
        channel.send('''display arp all \n''')
        time.sleep(1)
        buff = ''
        buff += channel.recv(9999)
        while buff.endswith('---- More ----'):
            channel.send(''' ''')
            time.sleep(1)
            buff += channel.recv(9999)
        if ip == '10.10.15.126':
            buff = buff.replace('  ---- More ----\x1b[42D                                          \x1b[42D','')
        else:
            buff = buff.replace('  ---- More ----\x1b[16D                \x1b[16D','')
        buff_li = buff.split('\r\n')
        print buff_li
        server_holeip[ip] = get_ip_mac_port(handle_re_strip(buff_li,ip),ip)
        
    print server_holeip
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    for ip, re_list in server_holeip.items():
        for li1 in re_list:
            print "ip: ", ip
            print "child_ip: ", li1[0]
            print "mac: ", li1[1]
            print "port: ", str(li1[2]).replace('\r\n', '')

    # 存储数据
    mysql = MySql('10.255.12.233', 6337, 'root', 'root','minxinyunwei', 'utf8')
    sql = "insert into equipment_ip_belong (ip,mac,port,father_ip,level)values(%s,%s,%s,%s,%s) on duplicate key update mac=%s,port=%s,level=%s;"
    for ip,re_list in server_holeip.items():
        mysql.run_sql(sql,[ip,'0','0','0','0','0','0','0'])
        for li1 in re_list:
            if li1[0] in ip_father_list:
                continue
            value_list = [li1[0],li1[1],str(li1[2]).replace('\r\n',''),ip,'1',li1[1],str(li1[2]).replace('\r\n',''),'1']
            mysql.run_sql(sql,value_list)
    print "start_time: ", start_time
    # 43 126
    print "end_time:   ", end_time
