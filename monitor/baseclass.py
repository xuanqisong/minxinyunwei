# -*- coding: utf-8 -*-

# monitor主类

# 服务器类
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


# 监控类
class CpuMemoryDisk(object):
    def __init__(self, ip, user, time, used, detail):
        self.__ip = ip
        self.__user = user
        self.__time = time
        self.__used = used
        self.__detail = detail

    def get_ip(self):
        return self.__ip

    def get_user(self):
        return self.__user

    def get_time(self):
        return self.__time

    def get_used(self):
        return self.__used

    def get_detail(self):
        return self.__detail


class Disk(CpuMemoryDisk):
    def __init__(self, ip, user, time, used, detail, disk_name):
        super(Disk, self).__init__(ip, user, time, used, detail)
        self.__disk_name = disk_name

    def get_disk_name(self):
        return self.__disk_name


# 报表基类
class HighChart(object):
    def __init__(self, faction_name, big_title_name, small_title_name, big_unit, small_unit):
        self.__faction_name = faction_name
        self.__big_title_name = big_title_name
        self.__small_title_name = small_title_name
        self.__big_unit = big_unit
        self.__small_unit = small_unit

    def get_faction_name(self):
        return self.__faction_name

    def get_big_title_name(self):
        return self.__big_title_name

    def get_small_title_name(self):
        return self.__small_title_name

    def get_big_unit(self):
        return self.__big_unit

    def get_small_unit(self):
        return self.__small_unit


# 报表曲线图类
class QuXianTu(HighChart):
    def __init__(self, categories, series, faction_name, big_title_name, small_title_name, big_unit, small_unit):
        super(QuXianTu, self).__init__(faction_name, big_title_name, small_title_name, big_unit, small_unit)
        self.__categories = categories
        self.__series = series

    def get_categories(self):
        return self.__categories

    def get_series(self):
        return self.__series


# 报表柱状图类
class ZhuZuangTu_Column_Drilldown(HighChart):
    def __init__(self, down_name, categories, data, faction_name, big_title_name, small_title_name, big_unit,
                 small_unit):
        super(ZhuZuangTu_Column_Drilldown, self).__init__(faction_name, big_title_name, small_title_name, big_unit,
                                                          small_unit)
        self.__categories = categories
        self.__data = data
        self.__down_name = down_name

    def get_categories(self):
        return self.__categories

    def get_data(self):
        return self.__data

    def get_down_name(self):
        return self.__down_name


# 报表柱状图，Column_DrillDown类
class Column_DrillDown_Child(object):
    def __init__(self, y, color, name, categories, data, child_color):
        self.__y = y
        self.__name = name
        self.__categories = categories
        self.__data = data
        self.__child_color = child_color
        self.__color = color

    def get_y(self):
        return self.__y

    def get_name(self):
        return self.__name

    def get_categories(self):
        return self.__categories

    def get_data(self):
        return self.__data

    def get_child_color(self):
        return self.__child_color

    def get_color(self):
        return self.__color


# 报表柱状图，分组柱状图categories
class ZhuZhuangTuGroupFather(HighChart):
    def __init__(self, categories, series, faction_name, big_title_name, small_title_name, big_unit,
                 small_unit):
        super(ZhuZhuangTuGroupFather, self).__init__(faction_name, big_title_name, small_title_name, big_unit,
                                                     small_unit)
        self.__categories = categories
        self.__series = series

    def get_categories(self):
        return self.__categories

    def get_series(self):
        return self.__series


class ZhuZhuangTuGroupCategories(object):
    def __init__(self, group_name, child_name):
        self.__group_name = group_name
        self.__child_name = child_name

    def get_group_name(self):
        return self.__group_name

    def get_child_name(self):
        return self.__child_name


# 报表柱状图，分组柱状图data
class ZhuZhuangTuGroupSeries(object):
    def __init__(self, color, data, name):
        self.__color = color
        self.__data = data
        self.__name = name

    def get_color(self):
        return self.__color

    def get_data(self):
        return self.__data

    def get_name(self):
        return self.__name

#磁盘柱状图，百分比数据类
class DiskPer(object):
    def __init__(self,ip,used,diskname):
        self.__ip = ip
        self.__diskname= diskname
        self.__used = used

    def get_ip(self):
        return self.__ip

    def get_diskname(self):
        return self.__diskname

    def get_used(self):
        return  self.__used

#饼状图类
class Pie(object):
    def __init__(self,ip,uname,uvalue,ename,evalue,fname):
        self.__ip = ip
        self.__uname = uname
        self.__uvalue = uvalue
        self.__ename = ename
        self.__evalue = evalue
        self.__fname = fname

    def get_ip(self):
        return self.__ip

    def get_uname(self):
        return  self.__uname

    def get_uvalue(self):
        return  self.__uvalue

    def get_ename(self):
        return self.__ename

    def get_evalue(self):
        return self.__evalue

    def get_fname(self):
        return self.__fname
