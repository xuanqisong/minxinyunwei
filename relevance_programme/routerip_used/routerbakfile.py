# -*- coding: utf-8 -*-

import time
import paramiko
import os


# 写文件函数
def write_file(filepath, txt, method):
    try:
        f = open(filepath, method)
        txt_type = str(type(txt))[7:12]
        if txt_type == 'tuple':
            for va in txt:
                f.write(str(va))
        elif txt_type == 'list':
            for va in txt:
                f.write(str(va))
        elif txt_type == 'dict':
            for va in txt.iteritems():
                f.write(str(va[0]))
                f.write(':')
                f.write(str(va[1]))
        else:
            f.write(str(txt))
        f.write('\n')
        f.close
    except Exception as e:
        print "write file error :", txt
        print "file path :", filepath
        print "error message :", e
        exit()


class ParamikoRun(object):
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

    def getsshconnect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, int(self.port), self.user, self.password)
        return ssh


if __name__ == "__main__":
    user = 'xuanqisong'
    password = 'xuanqisong@123'
    ip_father_list = ['10.10.15.126', '10.10.15.124', '10.10.15.125']
    # ip_father_list = ['10.10.15.126']
    paramikodi = {}
    ip_file = {}
    for ip in ip_father_list:
        paramikodi[ip] = ParamikoRun(ip, 22, user, password)

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
        # 清理无用字符
        if ip == '10.10.15.126':
            re_buff = re_buff.replace('  ---- More ----\x1b[42D                                          \x1b[42D', '')
        else:
            re_buff = re_buff.replace('  ---- More ----\x1b[16D                \x1b[16D', '')

        ip_file[ip] = re_buff


    # 获取文件名
    dir_name = os.path.dirname(os.path.abspath(__file__))
    time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 文件本身路径(出去文件名称)
    dir_name = os.path.dirname(os.path.abspath(__file__))
    # 获取文件上层目录
    dir_name_up = os.path.abspath(os.path.join(dir_name,os.path.pardir))
    # 获取文件上层目录
    dir_name_upup = os.path.abspath(os.path.join(dir_name_up,os.path.pardir))

    dir_name = dir_name_upup+'/servermanager/routerbakfile'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    dir_name = dir_name+ '/' + time_now
    os.mkdir(dir_name)
    ip_file_name = {}
    for ip in paramikodi:
        ip_file_name[ip] = dir_name + '/' + ip.replace('.','') + '_configuration.txt'

    # 写文件
    for ip, file_name in ip_file_name.items():
        txt = ip_file[ip]
        write_file(file_name,txt,'w')


