# -*- coding: utf-8 -*-
import MySQLdb
import global_function
import os

dir_name = os.path.dirname(os.path.abspath(__file__))

filepath = dir_name + '/log.txt'
mysql_ini = dir_name + '/mysql.ini'


# 系统mysql连接及方法
class MysqlDb(object):
    def __init__(self, db_name):
        self.db_name = db_name

    def get_connect(self):
        di = global_function.read_ini(mysql_ini, self.db_name)
        conn = MySQLdb.Connect(host=di['host'], port=int(di['port']), user=di['user'], passwd=di['passwd'], db=di['db'],
                               charset=di['charset'])
        return conn

    def run_sql(self, sql, value_li=''):
        try:
            conn = self.get_connect()

            try:
                cu = conn.cursor()
                if value_li != "":
                    cu.execute(sql, value_li)
                else:
                    cu.execute(sql)

                rs = cu.fetchall()
                conn.commit()
                cu.close()
                conn.close()
                global_function.write_file(filepath, sql, 'a+')
                return rs

            except Exception as e:
                global_function.write_file(filepath, "execute sql error: " + str(e), 'a+')
                conn.rollback()
                conn.close()
                return False

        except Exception as e:
            global_function.write_file(filepath, "get DB connect error: " + str(e), 'a+')
            return False
