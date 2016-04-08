# coding=utf-8
# 没有做到每周执行的计划任务
from threading import Thread
import global_function
import subprocess
from global_class import Singleton


class JobTable(object):
    def __init__(self, t_id, t_year, t_month, t_day, t_hour, t_minute, t_second, combine_time, function_name,
                 run_mark):
        self.id = t_id
        self.t_year = t_year
        self.t_mounth = t_month
        self.t_day = t_day
        self.t_hour = t_hour
        self.t_minute = t_minute
        self.t_second = t_second
        self.combine_time = combine_time
        self.function_name = function_name
        self.run_mari = run_mark


class GetWorkList(Thread, Singleton):
    def __init__(self, mysql, work_queue):
        Thread.__init__(self)
        self.mysql = mysql
        self.work_queue = work_queue
        self.old_time = ''

    def run(self):
        while True:
            sql = "select id, combine_time, function_name from job_table WHERE run_mark = '1'"
            re_li = global_function.tuple_to_list(self.mysql.run_sql(sql, ''))
            re_li = map(global_function.str_just, re_li)
            re_li = filter(global_function.judge_time, re_li)
            if len(re_li) > 0:
                if self.old_time != re_li[0][3]:
                    self.work_queue.put(re_li)
                    self.old_time = re_li[0][3]


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
