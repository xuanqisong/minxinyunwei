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

# job
mysql = MysqlDb('mysql-host')
work_queue = Queue.Queue(0)
getworklist = GetWorkList(mysql, work_queue)
allocationthread = AllocationThread(work_queue)
print "1"
getworklist.start()
allocationthread.start()
print "2"
# job
