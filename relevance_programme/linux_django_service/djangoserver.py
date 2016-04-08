#!/usr/bin/env python  

import sys, time
import commands
from service import Daemon


class MyDaemon(Daemon):
    def run(self):
        timer = time.localtime()
        time_django = time.strftime('%Y-%m-%d %H:%M:%s', timer)
        (re_num, re_txt) = commands.getstatusoutput(
            '/usr/local/bin/python /django/minxinyunwei/manage.py runserver 0.0.0.0:8080')
        sys.stdout.write("[%s]out_put:%s" % (re_num, re_txt))
        print 'abc'
        while True:
            sys.stdout.flush()
            time.sleep(1)


if __name__ == "__main__":
    daemon = MyDaemon('/django/log/django.pid', '/django/log/in.log', '/django/log/out.log', '/django/log/err.log')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
