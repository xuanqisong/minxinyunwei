# coding=utf-8
# 没有做到每周执行的计划任务
from threading import Thread
import global_function
import subprocess
from global_class import Singleton
import time
import os

file_base = os.path.dirname(__file__)


class GetWorkList(Thread, Singleton):
    def __init__(self, mysql, work_queue):
        Thread.__init__(self)
        self.mysql = mysql
        self.work_queue = work_queue
        self.old_time = ''

    def run(self):
        while True:
            time.sleep(0.5)
            sql = "select t_year,t_month,t_day,t_hour,t_minute,t_second,function_name from job_table WHERE run_mark = '1'"
            re_tu = self.mysql.run_sql(sql)
            global_function.update_time(self.mysql)
            if not re_tu:
                continue
            elif len(re_tu) < 1:
                continue
            re_li = map(global_function.str_just, re_tu)
            re_li = filter(global_function.judge_time, re_li)
            if len(re_li) > 0:
                global_function.write_file(file_base + "/job_log.txt", re_li, 'a')
                if self.old_time != re_li[0][1]:
                    self.work_queue.put(re_li)
                    self.old_time = re_li[0][1]


class AllocationThread(Thread, Singleton):
    def __init__(self, work_queue):
        Thread.__init__(self)
        self.work_queue = work_queue

    def run(self):
        while True:
            li = self.work_queue.get()
            print "run queue thread and thread li :", li
            for job in li:
                runfunction = RunFunction(job[2])
                runfunction.start()
            self.work_queue.task_done()


class RunFunction(Thread):
    def __init__(self, function_name):
        Thread.__init__(self)
        self.function_name = function_name

    def run(self):
        # print "run function function_name :", self.function_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # child = subprocess.Popen("python " + self.function_name) # windows
        # child.wait()
        # execfile(self.function_name)  # linux
        if str(str(self.function_name).split('/')[-1]).split('.')[-1] == "py":
            os.popen("python " + self.function_name)
        else:
            os.popen(self.function_name)
