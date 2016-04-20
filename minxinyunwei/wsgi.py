"""
WSGI config for minxinyunwei project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minxinyunwei.settings")

application = get_wsgi_application()


import Queue
from Tools.job import GetWorkList, AllocationThread

from Tools.DBtools import MysqlDb
from Tools import global_function

# job
mysql = MysqlDb('mysql-host')
sql = "SELECT * FROM job_table WHERE run_mark='9'"
re_tu = mysql.run_sql(sql)
if global_function.check_run_job(re_tu):
    global_function.update_time(mysql)
    work_queue = Queue.Queue(0)
    getworklist = GetWorkList(mysql, work_queue)
    allocationthread = AllocationThread(work_queue)
    print "1"
    getworklist.start()
    allocationthread.start()
    print "2"
# job
