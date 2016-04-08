# -*- coding=utf-8 -*-
from threading import Thread
import json
import time
import paramiko
from Tools import global_function, global_value
from Tools.global_class import Singleton, Singleton2


class Serverlist(object):
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

    def get_detail(self):
        return self.__detail


class Server(object):
    def __init__(self, ip, user, password, port, detail, group, state):
        self.__ip = ip
        self.__user = user
        self.__password = password
        self.__port = port
        self.__detail = detail
        self.__group = group
        self.__state = state

    def get_ip(self):
        return self.__ip

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def get_port(self):
        return self.__port

    def get_detail(self):
        return self.__detail

    def get_group(self):
        return self.__group

    def get_state(self):
        return self.__state


class WebSSHBase(object):
    def __init__(self, user, pas, ip, ipreplace, groupname, connectstatu, rectext, port):
        self.__user = user
        self.__ip = ip
        self.__ipreplace = ipreplace
        self.__pas = pas
        self.__groupname = groupname
        self.__rectext = rectext
        self.__connectstatu = connectstatu
        self.__port = port

    def get_user(self):
        return self.__user

    def get_ip(self):
        return self.__ip

    def get_ipreplace(self):
        return self.__ipreplace

    def get_groupname(self):
        return self.__groupname

    def get_connectstatu(self):
        return self.__connectstatu

    def get_rectext(self):
        return self.__rectext

    def get_pas(self):
        return self.__pas

    def get_port(self):
        return self.__port


# WebSSH类
class PRun(object):
    def __init__(self, ip, port, user, pas):
        self.ip = ip
        self.port = port
        self.user = user
        self.pas = pas
        self.ssh = [False, None]
        self.channel = [False,None]
        self.sftp = [False, None]

    def get_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh[1] = ssh

    def get_connect_ssh(self):
        if self.ssh[1] is None:
            self.get_ssh()
            try:
                self.ssh[1].connect(self.ip, int(self.port), self.user,
                                    global_function.decrypt(global_value.ENCRYPT_KEY_VALUE, self.pas))
                self.ssh[0] = True
            except Exception as e:
                self.ssh[1] = str(e)
        # else:
        #     try:
        #         self.ssh[1].connect(self.ip, int(self.port), self.user,
        #                             global_function.decrypt(global_value.ENCRYPT_KEY_VALUE, self.pas))
        #         self.ssh[0] = True
        #     except Exception as e:
        #         self.ssh[1] = str(e)

    def close_ssh(self):
        self.ssh[1].close()
        self.ssh[0] = False
        self.ssh[1] = None

    def get_connect_channel(self):
        self.get_connect_ssh()
        if not self.channel[0]:
            if not self.ssh[0]:
                self.channel = [False, None]
            else:
                self.channel = [True, self.ssh[1].invoke_shell()]

    def close_channel(self):
        self.channel[1].close()
        self.channel[0] = False
        self.channel[1] = None

    def get_connect_sftp(self):
        self.get_connect_ssh()
        if self.ssh[0]:
            try:
                t = paramiko.Transport((self.ip, int(self.port)))
                t.connect(username=self.user,
                          password=global_function.decrypt(global_value.ENCRYPT_KEY_VALUE, self.pas))
                self.sftp[1] = paramiko.SFTPClient.from_transport(t)
                self.sftp[0] = True
            except Exception as e:
                self.sftp[1] = str(e)

    def close_sftp(self):
        self.sftp[1].close()
        # self.sftp = [False, None]
        self.sftp[0] = False
        self.sftp[1] = None


class PRec(Thread):
    def __init__(self, ip, p_run):
        Thread.__init__(self)
        self.ip = ip
        self.p_run = p_run
        # self.ssh = [False, None]
        # self.channel = None
        self.monitor = True
        self.inner_pause = False
        self.rec_text = ''
        self.error_text = ''

    def run(self):
        # self.p_run.get_connect_channel()
        # self.ssh = self.p_run.ssh
        # self.channel = self.p_run.channel
        while True:
            # self.ssh = self.p_run.ssh
            # self.channel = self.p_run.channel
            try:
                while self.inner_pause:
                    pass

                if self.p_run.channel[0]:
                    while self.p_run.channel[1].recv_ready():
                        self.rec_text += self.p_run.channel[1].recv(2048)
                        # print self.rec_text

            except Exception as e:
                self.error_text += str(e)

            if not self.monitor:
                break


class PSend(Thread):
    def __init__(self, ip, p_run):
        Thread.__init__(self)
        self.ip = ip
        self.p_run = p_run
        # self.ssh = [False, None]
        # self.channel = None
        self.monitor = True
        self.send_text = ''
        self.error_text = ''

    def run(self):
        # self.p_run.get_connect_channel()
        # self.ssh = self.p_run.ssh
        # self.channel = self.p_run.channel
        while True:
            # self.ssh = self.p_run.ssh
            # self.channel = self.p_run.channel
            try:
                if self.p_run.channel[0]:
                    if len(self.send_text) > 0:
                        # print self.send_text
                        self.p_run.channel[1].send(self.send_text + " --color=never" + "\n")
                        self.send_text = ''

            except Exception as e:
                self.error_text += str(e)

            if not self.monitor:
                break


class FileSendReceive(Thread):
    def __init__(self, ip, p_run):
        Thread.__init__(self)
        self.ip = ip
        self.p_run = p_run
        # self.sftp = [False, None]
        # self.ssh = None
        self.percent = 0
        self.start_t = False
        self.monitor = True
        self.file_type = ''
        self.local_path = ''
        self.remote_path = ''
        self.error_text = ''

    def run(self):
        # self.p_run.get_connect_sftp()

        while True:
            # self.ssh = self.p_run.ssh
            # self.sftp = self.p_run.sftp
            # if not self.p_run.sftp[0]:
            #     self.p_run.get_connect_sftp()
            try:
                if self.p_run.ssh[0]:
                    if self.p_run.sftp[0]:
                        if self.start_t:
                            try:
                                if self.file_type == "send":
                                    self.p_run.sftp[1].put(self.local_path, self.remote_path, self.count_percent, False)
                                elif self.file_type == "receive":
                                    self.p_run.sftp[1].get(self.remote_path, self.local_path, self.count_percent)
                            except Exception as e:
                                self.error_text += str(e)

                            self.start_t = False

            except Exception as e:
                self.error_text += str(e)

            if not self.monitor:
                break

    def count_percent(self, size, file_size):
        self.percent = str(int((float(size) / file_size) * 100))


# 监控线程
class Monitor(Thread):
    # __metaclass__ = Singleton2

    def __del__(self):
        self.client = None
        self.server_ip_list = None
        self.send_di = None
        self.monitor = None
        self.pause = None
        self.thread_file_send_receive = None
        self.thread_p_rec = None
        self.thread_p_send = None

    def __init__(self):
        Thread.__init__(self)
        self.client = None
        self.server_ip_list = []
        self.send_di = {}
        self.monitor = True
        self.pause = True
        self.prun = {}
        self.thread_p_rec = {}
        self.thread_p_send = {}
        self.thread_file_send_receive = {}

    def run(self):
        while True:
            time.sleep(1)
            for ip in self.server_ip_list:
                self.send_di[ip] = {}
                # 暂停接收
                self.thread_p_rec[ip].inner_pause = True
                self.send_di[ip]['recmessage'] = self.thread_p_rec[ip].rec_text
                # 清空接收字符串
                self.thread_p_rec[ip].rec_text = ''
                # 开启接收
                self.thread_p_rec[ip].inner_pause = False
                self.send_di[ip]['syserror'] = ''

                if self.thread_file_send_receive[ip].start_t:
                    if self.thread_file_send_receive[ip].file_type == 'send':
                        self.send_di[ip]['uploaddownloadfile'] = {'statu': 's',
                                                                  'percent': self.thread_file_send_receive[ip].percent}
                    elif self.thread_file_send_receive[ip].file_type == 'receive':
                        self.send_di[ip]['uploaddownloadfile'] = {'statu': 'r',
                                                                  'percent': self.thread_file_send_receive[ip].percnet}
                else:
                    self.send_di[ip]['uploaddownloadfile'] = {'statu': 'n', 'percent': '0'}
                    self.send_di[ip]['syserror'] += self.thread_file_send_receive[ip].error_text
                    self.thread_file_send_receive[ip].error_text = ''

                if self.thread_p_rec[ip].error_text != "":
                    self.send_di[ip]['syserror'] += "paramikorec: " + self.thread_p_rec[ip].error_text
                    self.thread_p_rec[ip].error_text = ""

                if self.thread_p_send[ip].error_text != "":
                    self.send_di[ip]['syserror'] += "paramikosend: " + self.thread_p_send[ip].error_text
                    self.thread_p_send[ip].error_text = ""

                if self.thread_p_rec[ip].is_alive():
                    if self.thread_p_rec[ip].p_run.ssh[0]:
                        self.send_di[ip]['connectstatu'] = '1'
                    else:
                        self.send_di[ip]['connectstatu'] = '9'
                else:
                    self.send_di[ip]['connectstatu'] = '2'

            di_json = json.dumps(self.send_di)
            # try:
            #     for client in self.client:
            #         client.send(di_json)
            # except Exception as e:
            #     print "client: ", e
            #     print self.client
            self.client.send(di_json)

            if not self.monitor:
                # 监控线程结束，子线程结束
                for ip, p_rec in self.thread_p_rec.items():
                    p_rec.monitor = False
                for ip, p_send in self.thread_p_send.items():
                    p_send.monitor = False
                for ip, file_send_receive in self.thread_file_send_receive.items():
                    file_send_receive.sftp[1].close()

                while True:
                    p_rec_alive_list = []
                    p_send_alive_list = []
                    for ip, p_rec in self.thread_p_rec.items():
                        p_rec_alive_list.append(p_rec.is_alive())
                    for ip, p_send in self.thread_p_send.items():
                        p_send_alive_list.append(p_send.is_alive())

                    if True not in p_rec_alive_list and True not in p_send_alive_list:
                        break

                break
