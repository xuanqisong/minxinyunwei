# coding=utf-8
# 没有做到每周执行的计划任务
from threading import Thread
import global_function
import subprocess
from global_class import Singleton


class GetWorkList(Thread, Singleton):
    def __init__(self, mysql, work_queue):
        Thread.__init__(self)
        self.mysql = mysql
        self.work_queue = work_queue
        self.old_time = ''

    def run(self):
        while True:
            sql = "select t_year,t_month,t_day,t_hour,t_minute,t_second,function_name from job_table WHERE run_mark = '1'"
            re_tu = self.mysql.run_sql(sql)
            if not re_tu:
                continue
            elif len(re_tu) < 1:
                continue
            re_li = map(global_function.str_just, re_tu)
            re_li = filter(global_function.judge_time, re_li)
            if len(re_li) > 0:
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
                runfunction = RunFunction(job[1])
                runfunction.start()
            self.work_queue.task_done()


class RunFunction(Thread):
    def __init__(self, function_name):
        Thread.__init__(self)
        self.function_name = function_name

    def run(self):
        # print "run function function_name :", self.function_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        child = subprocess.Popen("python " + self.function_name)
        child.wait()
