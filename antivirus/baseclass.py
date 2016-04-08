# -*- coding: utf-8 -*-

import pyclamd
import time
from threading import Thread
import json
import use_factions


# job class
class TableJob(object):
    def __init__(self, sql_list):
        self.sql_list = sql_list
        self.id = ''
        self.t_year = ''
        self.t_month = ''
        self.t_day = ''
        self.t_hour = ''
        self.t_minute = ''
        self.t_second = ''
        self.combine_time = ''
        self.function_name = ''
        self.run_mark = ''

    def binding_value(self):
        self.id = self.sql_list[0]
        self.t_year = self.sql_list[1]
        self.t_month = self.sql_list[2]
        self.t_day = self.sql_list[3]
        self.t_hour = self.sql_list[4]
        self.t_minute = self.sql_list[5]
        self.t_second = self.sql_list[6]
        self.combine_time = self.sql_list[7]
        self.function_name = self.sql_list[8]
        self.run_mark = self.sql_list[9]


class Scan(Thread):
    def __init__(self, ip, scan_type, file):
        Thread.__init__(self)
        self.ip = ip
        self.scan_type = scan_type
        self.file = file
        self.connstr = ""
        self.scanresult = ""

    def run(self):
        try:
            cd = pyclamd.ClamdNetworkSocket(self.ip, 3310)
            if cd.ping():
                self.connstr = self.ip + " connection [OK]"
                cd.reload()
                if self.scan_type == "contscan_file":
                    self.scanresult = "{0}\n".format(cd.contscan_file(self.file))
                elif self.scan_type == "multiscan_file":
                    self.scanresult = "{0}\n".format(cd.multiscan_file(self.file))
                elif self.scan_type == "scan_file":
                    self.scanresult = "{0}\n".format(cd.scan_file(self.file))
                time.sleep(1)
            else:
                self.connstr = self.ip + " ping error,exit"
                return
        except Exception, e:
            self.connstr = self.ip + " " + str(e)


class ClamAV(Thread):
    def __init__(self, ip, scan_type, dir_name):
        Thread.__init__(self)
        self.ip = ip
        self.scan_type = scan_type
        self.connstr = ""
        self.scanresult = ""
        self.cns = ""
        self.file = dir_name
        self.tf = True

    def get_cns(self):
        try:
            cns = pyclamd.ClamdNetworkSocket(str(self.ip), 3310)
            self.cns = cns
        except Exception, e:
            self.tf = False
            self.connstr = self.ip + " " + str(e)

    def run(self):
        try:
            if self.scan_type == "contscan_file":
                self.scanresult = "{0}\n".format(self.cns.contscan_file(self.file))
            elif self.scan_type == "multiscan_file":
                self.scanresult = "{0}\n".format(self.cns.multiscan_file(self.file))
            elif self.scan_type == "scan_file":
                self.scanresult = "{0}\n".format(self.cns.scan_file(self.file))
            time.sleep(1)
        except Exception, e:
            self.connstr = self.ip + " " + str(e)

    def shutdown_cns(self):
        self.cns.shutdown()


class RunStatuHtml(object):
    def __init__(self, ip, dir_name, div_id):
        self.__ip = ip
        self.__dir_name = dir_name
        self.__div_id = div_id

    def get_ip(self):
        return self.__ip

    def get_dir_name(self):
        return self.__dir_name

    def get_div_id(self):
        return self.__div_id


class WhileCheckClamavRun(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.client = None
        self.message = None
        self.clamavlist = []

    def get_clamavlist(self, li):
        for clamav in li:
            self.clamavlist.append(clamav)

    def run(self):
        # 开始
        di = {'message': "start"}
        di_str = json.dumps(di)
        self.client.send(di_str)

        time.sleep(3)
        # 启动线程

        # 开启查毒连接
        for clamav in self.clamavlist:
            clamav.get_cns()

        # 向前台发送联通回信
        di = {'message': "get server connect!"}
        for clamav in self.clamavlist:
            ip_name = str(clamav.ip).replace('.', '')
            file_name = str(clamav.file).replace('/', '')
            if clamav.tf:
                if clamav.cns.ping():
                    di[ip_name + file_name] = '1'
            else:
                di[ip_name + file_name] = '4'
        di_str = json.dumps(di)
        self.client.send(di_str)
        time.sleep(3)
        # 开启线程,回馈网页，执行中
        di = {'message': "is checking!"}
        for clamav in self.clamavlist:
            ip_name = str(clamav.ip).replace('.', '')
            file_name = str(clamav.file).replace('/', '')
            if clamav.cns.ping():
                clamav.start()
                di[ip_name + file_name] = '2'
        di_str = json.dumps(di)
        self.client.send(di_str)
        time.sleep(3)

        while True:
            check_thread_list = []
            di = {'message': ''}
            for clamav in self.clamavlist:
                ip_name = str(clamav.ip).replace('.', '')
                file_name = str(clamav.file).replace('/', '')
                check_thread_list.append(clamav.is_alive())
                if clamav.is_alive():
                    di[ip_name + file_name] = '2'
                    di['message'] += clamav.ip + ": is checking! </br>"
                else:
                    di[ip_name + file_name] = '3'
                    print "3"
                    di['message'] += clamav.ip + ": " + use_factions.check_rsclamavstr(clamav.scanresult) + "</br>"

            di_str = json.dumps(di)
            self.client.send(di_str)

            if True not in check_thread_list:
                break

            if self.message == 'stop':
                for clamav in self.clamavlist:
                    clamav.shutdown_cns()
                break

            time.sleep(5)

        while True:
            time.sleep(2)
            di = {'message': ''}
            check_thread_alive = []
            for clamav in self.clamavlist:
                check_thread_alive.append(clamav.is_alive())

            if True not in check_thread_alive:
                for clamav in self.clamavlist:
                    ip_name = str(clamav.ip).replace('.', '')
                    file_name = str(clamav.file).replace('/', '')
                    di[ip_name + file_name] = '5'
                    di['message'] += clamav.ip + ": antivirus shutdown! </br>"

                break
            else:
                for clamav in self.clamavlist:
                    ip_name = str(clamav.ip).replace('.', '')
                    file_name = str(clamav.file).replace('/', '')
                    di[ip_name + file_name] = '6'
                    di['message'] += clamav.ip + ": is shutdowning! </br>"
            di_str = json.dumps(di)
            self.client.send(di_str)

        di['message'] = 'check down!'
        di_str = json.dumps(di)
        self.client.send(di_str)
