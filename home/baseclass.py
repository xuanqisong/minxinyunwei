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
        self.function_name = str(self.sql_list[7]).split('/')[(len(str(self.sql_list[7]).split('/')) - 1)]
        self.run_mark = self.sql_list[8]
