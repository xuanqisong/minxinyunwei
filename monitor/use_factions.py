# -*- coding: utf-8 -*-
from Tools import global_function
from Tools.DBtools import MysqlDb

from monitor.baseclass import *
from string import punctuation


# monitor通用函数
# 获取数据时间最大最小值
def get_startendtime():
    sql_cpu = "select min(time),max(time) FROM statu_cpu "
    sql_disk = "select min(time),max(time) FROM  statu_disk"
    sql_memory = "select min(time),max(time) FROM  statu_memory"
    start_time = ''
    end_time = ''
    mysql = MysqlDb('mysql-host')

    rs_tu = mysql.run_sql(sql_cpu, '')
    rs_li = global_function.tuple_to_list(rs_tu)

    for li in rs_li:
        start_time = li[0]
        end_time = li[1]

    rs_tu = mysql.run_sql(sql_disk, '')
    rs_li = global_function.tuple_to_list(rs_tu)

    for li in rs_li:
        if li[0] < start_time:
            start_time = li[0]
        if li[1] > end_time:
            start_time = li[1]

    rs_tu = mysql.run_sql(sql_memory, '')
    rs_li = global_function.tuple_to_list(rs_tu)

    for li in rs_li:
        if li[0] < start_time:
            start_time = li[0]
        if li[1] > end_time:
            start_time = li[1]
    return [start_time[:10], end_time[:10]]


# 系统单属性监控，曲线图数据查询拼接（待完善）
def get_cpu_ip(ip, stat):
    li2 = []

    if stat == "cpu":
        sql = "select ip,date_format(time,'%%Y-%%m-%%d %%H:%%i:%%S'),used from statu_cpu where ip = %s"
    else:
        sql = "select ip,date_format(time,'%%Y-%%m-%%d %%H:%%i:%%S'),used from statu_cpu where ip = %s"

    mysql = MysqlDb('mysql-host')
    rs_tu = mysql.run_sql(sql, ip)
    rs_li = global_function.tuple_to_list(rs_tu)
    cpuipuserlist = []
    for li in rs_li:
        a = CpuMemoryDisk(li[0], '', li[1], li[2], ip)
        cpuipuserlist.append(a)

    quxian_categories = []
    quxian_data = ''
    da = []
    for cpuipuser in cpuipuserlist:
        i = 0
        quxian_categories.append(cpuipuser.get_time())
        da.append(float(cpuipuser.get_used()))
        if i == 0:
            quxian_data = "{name: '" + cpuipuser.get_ip() + "',data: "

    quxian_data = quxian_data + str(da) + "}"
    li2.append(quxian_categories)
    li2.append(quxian_data)
    return li2


# 获取服务器列表
def get_serverlist():
    sql_server_list = "select * from server_list WHERE servertype='1'"

    mysql = MysqlDb('mysql-host')

    rs_tu = mysql.run_sql(sql_server_list, '')
    rs_li = global_function.tuple_to_list(rs_tu)

    servernamelist = []

    for li in rs_li:
        a = Server(li[0], li[1], li[2], li[3], li[4], li[5], li[6])
        servernamelist.append(a)

    return servernamelist


# 获取服务器，组别列表
def get_server_grouplist():
    sql = "SELECT DISTINCT(`group`) FROM server_list WHERE servertype='1'"

    mysql = MysqlDb('mysql-host')
    rs_tu = mysql.run_sql(sql, '')
    rs_li = global_function.tuple_to_list(rs_tu)
    return rs_li


# 获取服务器组，组内成员属性
def get_group_ip_list(group_name):
    server_list = []
    sql = "SELECT * FROM server_list WHERE `group` = %s AND servertype='1'"

    mysql = MysqlDb('mysql-host')
    rs_tu = mysql.run_sql(sql, group_name)
    rs_li = global_function.tuple_to_list(rs_tu)

    for li in rs_li:
        server_list.append(Server(li[0], li[1], li[2], li[3], li[4], li[5], li[6]))

    return server_list


def get_server_ip(ip):
    server_list = []
    sql = "SELECT * FROM server_list WHERE ip = %s AND servertype='1'"

    mysql = MysqlDb('mysql-host')
    rs_tu = mysql.run_sql(sql, ip)
    rs_li = global_function.tuple_to_list(rs_tu)

    for li in rs_li:
        server_list.append(Server(li[0], li[1], li[2], li[3], li[4], li[5], li[6]))

    return server_list


# 获取日报报表日期列表
def get_monitor_day_list():
    mysql = MysqlDb('mysql-host')
    monitor_day_list = []

    sql_statu_cpu = "SELECT  DISTINCT(date_format(time,'%Y')) FROM statu_cpu "
    sql_statu_memory = "SELECT  DISTINCT(date_format(time,'%Y')) FROM statu_memory "
    sql_statu_disk = "SELECT  DISTINCT(date_format(time,'%Y')) FROM statu_disk "

    rs_tu_cpu = mysql.run_sql(sql_statu_cpu, '')
    rs_tu_memory = mysql.run_sql(sql_statu_memory, '')
    rs_tu_disk = mysql.run_sql(sql_statu_disk, '')

    rs_li_cpu = global_function.tuple_to_list(rs_tu_cpu)
    rs_li_memory = global_function.tuple_to_list(rs_tu_memory)
    rs_li_disk = global_function.tuple_to_list(rs_tu_disk)

    for va in rs_li_cpu:
        if va[0] not in monitor_day_list:
            monitor_day_list.append(va[0])
    for va in rs_li_disk:
        if va[0] not in monitor_day_list:
            monitor_day_list.append(va[0])

    for va in rs_li_memory:
        if va[0] not in monitor_day_list:
            monitor_day_list.append(va[0])

    return monitor_day_list


def get_monitor_time_list():
    mysql = MysqlDb('mysql-host')
    monitor_day_list = []

    sql_statu_cpu = "SELECT  DISTINCT(date_format(time,'%Y-%m-%d')) FROM statu_cpu "
    sql_statu_memory = "SELECT  DISTINCT(date_format(time,'%Y-%m-%d')) FROM statu_memory "
    sql_statu_disk = "SELECT  DISTINCT(date_format(time,'%Y-%m-%d')) FROM statu_disk "

    rs_tu_cpu = mysql.run_sql(sql_statu_cpu, '')
    rs_tu_memory = mysql.run_sql(sql_statu_memory, '')
    rs_tu_disk = mysql.run_sql(sql_statu_disk, '')

    rs_li_cpu = global_function.tuple_to_list(rs_tu_cpu)
    rs_li_memory = global_function.tuple_to_list(rs_tu_memory)
    rs_li_disk = global_function.tuple_to_list(rs_tu_disk)

    for va in rs_li_cpu:
        if va[0] not in monitor_day_list:
            monitor_day_list.append(va[0])
    for va in rs_li_disk:
        if va[0] not in monitor_day_list:
            monitor_day_list.append(va[0])

    for va in rs_li_memory:
        if va[0] not in monitor_day_list:
            monitor_day_list.append(va[0])

    return monitor_day_list


# 拼接曲线图数据
def make_quxiantu_data(server_ip_list, attribute, monitor_day):
    quxiantu_data = get_server_statu_data(server_ip_list, attribute, monitor_day)
    quxiantu_list = []

    for k, v in quxiantu_data.items():
        faction_name = "quxiantu" + str(k).translate(None, punctuation) + attribute
        big_title_name = attribute
        small_title_name = k
        big_unit = "%"
        small_unit = "%"

        data = []
        categories = []
        series = ''
        for cpuipuser in v:
            categories.append(cpuipuser.get_time())
            data.append(float(cpuipuser.get_used()))
            series = "{name: '" + cpuipuser.get_detail() + "',data: "

        series = series + str(data) + "}"
        a = QuXianTu(categories, series, faction_name, big_title_name, small_title_name, big_unit, small_unit)
        quxiantu_list.append(a)

    return quxiantu_list


def make_quxiantu_data_startend(server_ip_list, attribute, start_time, end_time):
    quxiantu_data = get_server_statu_data_startend(server_ip_list, attribute, start_time, end_time)
    quxiantu_list = []

    for k, v in quxiantu_data.items():
        faction_name = "quxiantu" + str(k).translate(None, punctuation) + attribute
        big_title_name = attribute
        small_title_name = k
        big_unit = "%"
        small_unit = "%"

        data = []
        categories = []
        series = ''
        for cpuipuser in v:
            categories.append(cpuipuser.get_time())
            data.append(float(cpuipuser.get_used()))
            series = "{name: '" + cpuipuser.get_detail() + "',data: "

        series = series + str(data) + "}"
        a = QuXianTu(categories, series, faction_name, big_title_name, small_title_name, big_unit, small_unit)
        quxiantu_list.append(a)

    return quxiantu_list


def make_quxiantu_data_startend(server_ip_list, attribute, start_time, end_time):
    quxiantu_data = get_server_statu_data_startend(server_ip_list, attribute, start_time, end_time)
    quxiantu_list = []

    for k, v in quxiantu_data.items():
        faction_name = "quxiantu" + str(k).translate(None, punctuation) + attribute
        big_title_name = attribute + ":" + str(start_time) + " TO " + str(end_time)
        small_title_name = k
        big_unit = "%"
        small_unit = "%"

        data = []
        categories = []
        series = ''
        for cpuipuser in v:
            categories.append(cpuipuser.get_time())
            data.append(float(cpuipuser.get_used()))
            series = "{name: '" + cpuipuser.get_detail() + "',data: "

        series = series + str(data) + "}"
        a = QuXianTu(categories, series, faction_name, big_title_name, small_title_name, big_unit, small_unit)
        quxiantu_list.append(a)

    return quxiantu_list


# 拼接柱状图数据
def make_zhuzhuangtu_data(server_ip_list, attribute, monitor_day):
    column_drilldown_child_list = make_colunm_drilldown_child_data(server_ip_list, attribute, monitor_day)

    down_name = "DISK"
    categories = []
    for server in server_ip_list:
        categories.append(server.get_detail())
    data = column_drilldown_child_list
    faction_name = "zhuzhuangtu"
    big_title_name = "DISK"
    small_title_name = "used %"
    big_unit = "%"
    small_unit = "%"

    zhuzhuangtu_list = []

    zhuzhuangtu_list.append(
            ZhuZuangTu_Column_Drilldown(down_name, categories, data, faction_name, big_title_name, small_title_name,
                                        big_unit,
                                        small_unit))

    return zhuzhuangtu_list


# 拼接柱状图子数据
def make_colunm_drilldown_child_data(server_ip_list, attribute, monitor_day):
    column_dirlldown_child_data = get_server_statu_data(server_ip_list, attribute, monitor_day)
    column_drilldown_child_list = []
    i_num = 0
    for ip, cpumemorydisklist in column_dirlldown_child_data.items():
        categories = []
        data = []
        name = ''
        child_color = ''
        color = ''

        num = 0
        for cpumemorydisk in cpumemorydisklist:
            name = str(cpumemorydisk.get_ip()) + cpumemorydisk.get_detail()
            categories.append(cpumemorydisk.get_time())
            data.append(float(cpumemorydisk.get_used()))
            child_color = "colors[" + str(i_num) + "]"
            color = "colors[" + str(i_num) + "]"

        for i in data:
            num += float(i)
        y = str(num / len(data))[:5]
        column_drilldown_child_list.append(Column_DrillDown_Child(y, color, name, categories, data, child_color))
        i_num += 1
    return column_drilldown_child_list


# 拼接分组柱状图数据
def make_zhuzhuangtu_group_date(server_ip_list, monitor_day, disk_name_di):
    categories_str = ''
    series_list = []
    value_len = 0
    check_num = 0
    ip_disk_name = make_zhuzhuangtu_group_child_di(server_ip_list, monitor_day, disk_name_di)

    for ip in ip_disk_name:
        value_len += len(ip_disk_name[ip])

    # 获取颜色序列
    color_num = len(ip_disk_name)
    color_list = global_function.get_color(color_num)
    color_num = 0

    for ip, disk_name_data_di in ip_disk_name.items():
        child_name_list = []
        series_data_list = []
        for i in range(0, value_len):
            series_data_list.append('')

        for disk_name, used in disk_name_data_di.items():
            child_name_list.append(disk_name)
            series_data_list[check_num] = float("%.2f" % used)
            check_num += 1

        series_list.append(ZhuZhuangTuGroupSeries(color_list[color_num], series_data_list, ip))
        for li in child_name_list:
            categories_str += '"' + li + '"' + ','

        color_num += 1
    categories_str = categories_str[:-1]
    zhuzhuangtugroupfather = ZhuZhuangTuGroupFather(categories_str, series_list, 'disk_zhuzhuangtu', '硬盘使用百分比', 'disk',
                                                    '%', '%')

    return zhuzhuangtugroupfather


# 拼接分组柱状图子数据
def make_zhuzhuangtu_group_child_di(server_ip_list, monitor_day, disk_name_di):
    ip_disk_name = {}
    server_data_di = get_group_server_disk_data(server_ip_list, monitor_day)

    for ip, diskperlist in server_data_di.items():
        disk_name_data = {}
        for diskper in diskperlist:
            disk_name_data[diskper.get_diskname()] = diskper.get_used()

        ip_disk_name[ip] = disk_name_data

    # 清除未选中磁盘名称
    remove_ip_name = {}
    remove_ip = []
    for ip, disk_name_data_di in ip_disk_name.items():

        try:
            disk_name_list = disk_name_di[ip]
        except Exception as e:
            remove_ip.append(ip)
            continue
        for name in disk_name_data_di:

            if name not in disk_name_list:
                if ip not in remove_ip_name:
                    remove_ip_name[ip] = [name]
                else:
                    remove_ip_name[ip].append(name)

    for ip, namelist in remove_ip_name.items():
        for name in namelist:
            del ip_disk_name[ip][name]

    for ip in remove_ip:
        del ip_disk_name[ip]

    return ip_disk_name


# 获取日报当天分组柱状图数据
def get_group_server_disk_data(server_ip_list, monitor_day):
    mysql = MysqlDb('mysql-host')
    server_data_di = {}
    for server in server_ip_list:
        diskperlist = []
        # sql = "select ip,date_format(time,'%%H:%%i:%%S'),used,disk_name from statu_disk where ip = %s AND date_format(time,'%%Y-%%m-%%d')=%s"
        # sql = "select ip,date_format(time,'%%H:%%i:%%S'),used,disk_name from statu_disk where ip = %s AND date_format(time,'%%Y-%%m-%%d')=%s AND disk_name <>''"
        sql = "SELECT AVG(used),disk_name,ip from statu_disk where ip = %s AND date_format(time,'%%Y-%%m-%%d')=%s AND disk_name <>'' GROUP BY disk_name"
        rs_tu = mysql.run_sql(sql, [server.get_ip(), monitor_day])
        rs_li = global_function.tuple_to_list(rs_tu)
        for li in rs_li:
            # cpumemorydisklist.append(Disk(li[0], server.get_user(), li[1], li[2], server.get_detail(), li[3]))
            diskperlist.append(DiskPer(li[2], float(li[0]), li[1]))
        server_data_di[server.get_ip()] = diskperlist
    return server_data_di


# 获取日报当天时间函数
def get_server_statu_data(server_ip_list, attribute, monitor_day):
    mysql = MysqlDb('mysql-host')
    statu_data_di = {}
    for server in server_ip_list:
        cpumemorydisklist = []
        if attribute == "CPU":
            sql = "select ip,date_format(time,'%%H:%%i:%%S'),used from statu_cpu where ip = %s AND date_format(time,'%%Y-%%m-%%d')=%s"
        elif attribute == "MEMORY":
            sql = "select ip,date_format(time,'%%H:%%i:%%S'),used from statu_memory where ip = %s AND date_format(time,'%%Y-%%m-%%d')=%s"
        elif attribute == "DISK":
            sql = "select ip,date_format(time,'%%H:%%i:%%S'),used from statu_disk where ip = %s AND  date_format(time,'%%Y-%%m-%%d')=%s"
        rs_tu = mysql.run_sql(sql, [server.get_ip(), monitor_day])
        rs_li = global_function.tuple_to_list(rs_tu)
        for li in rs_li:
            a = CpuMemoryDisk(li[0], server.get_user(), li[1], li[2], server.get_detail())
            cpumemorydisklist.append(a)
        statu_data_di[server.get_ip()] = cpumemorydisklist

    return statu_data_di


def get_server_statu_data_startend(server_ip_list, attribute, start_time, end_time):
    mysql = MysqlDb('mysql-host')
    statu_data_di = {}
    for server in server_ip_list:
        cpumemorydisklist = []
        if attribute == "CPU":
            sql = "select ip,date_format(time,'%%Y-%%m-%%d/%%H:%%i:%%S'),used from statu_cpu where ip = %s AND date_format(time,'%%Y-%%m-%%d')>=%s AND date_format(time,'%%Y-%%m-%%d')<%s"
        elif attribute == "MEMORY":
            sql = "select ip,date_format(time,'%%Y-%%m-%%d/%%H:%%i:%%S'),used from statu_memory where ip = %s AND date_format(time,'%%Y-%%m-%%d')>=%s AND date_format(time,'%%Y-%%m-%%d')<%s"
        elif attribute == "DISK":
            sql = "select ip,date_format(time,'%%Y-%%m-%%d/%%H:%%i:%%S'),used from statu_disk where ip = %s AND  date_format(time,'%%Y-%%m-%%d')>=%s AND date_format(time,'%%Y-%%m-%%d')<%s"
        rs_tu = mysql.run_sql(sql, [server.get_ip(), start_time, end_time])
        rs_li = global_function.tuple_to_list(rs_tu)
        for li in rs_li:
            a = CpuMemoryDisk(li[0], server.get_user(), li[1], li[2], server.get_detail())
            cpumemorydisklist.append(a)
        statu_data_di[server.get_ip()] = cpumemorydisklist

    return statu_data_di


# 获取时间段监控数据
def get_server_statu_data_startend(server_ip_list, attribute, start_time, end_time):
    mysql = MysqlDb('mysql-host')
    statu_data_di = {}
    for server in server_ip_list:
        cpumemorydisklist = []
        if attribute == "CPU":
            sql = "select ip,date_format(time,'%%Y-%%m-%%d/%%H:%%i:%%S'),used from statu_cpu where ip = %s AND date_format(time,'%%Y-%%m-%%d')>=%s AND date_format(time,'%%Y-%%m-%%d')<%s"
        elif attribute == "MEMORY":
            sql = "select ip,date_format(time,'%%Y-%%m-%%d/%%H:%%i:%%S'),used from statu_memory where ip = %s AND date_format(time,'%%Y-%%m-%%d')>=%s AND date_format(time,'%%Y-%%m-%%d')<%s"
        elif attribute == "DISK":
            sql = "select ip,date_format(time,'%%Y-%%m-%%d/%%H:%%i:%%S'),used from statu_disk where ip = %s AND  date_format(time,'%%Y-%%m-%%d')>=%s AND date_format(time,'%%Y-%%m-%%d')<%s"
        rs_tu = mysql.run_sql(sql, [server.get_ip(), start_time, end_time])
        rs_li = global_function.tuple_to_list(rs_tu)
        for li in rs_li:
            a = CpuMemoryDisk(li[0], server.get_user(), li[1], li[2], server.get_detail())
            cpumemorydisklist.append(a)
        statu_data_di[server.get_ip()] = cpumemorydisklist

    return statu_data_di


# 曲线图单属性拼接
def combine_show(li):
    categories = ''
    series = ''
    faction_name = ''
    big_title_name = ''
    small_title_name = ''
    big_unit = ''
    small_unit = ''
    categories_len = 0

    for quxiantu in li:
        if len(quxiantu.get_series()) > 3:
            series = series + "," + quxiantu.get_series()

        if categories_len < len(quxiantu.get_categories()):
            categories = quxiantu.get_categories()

        faction_name = quxiantu.get_faction_name()
        big_title_name = quxiantu.get_big_title_name()
        small_title_name = ""
        big_unit = quxiantu.get_big_unit()
        small_unit = quxiantu.get_small_unit()
        categories_len = len(quxiantu.get_categories())

    quxiantu_class = QuXianTu(categories, series[1:], faction_name, big_title_name, small_title_name, big_unit,
                              small_unit)

    return quxiantu_class


# 饼状图
def get_pie_date(server_ip_list, monitor_day, disk_name_di):
    rt_di = {}

    ip_disk_name = make_zhuzhuangtu_group_child_di(server_ip_list, monitor_day, disk_name_di);

    for ip, disk_value in ip_disk_name.items():

        for disk_name, value in disk_value.items():
            evalue = 100 - value
            ip_name = str(ip).replace('.', '')
            disk_rname = str(disk_name).replace('/', '')
            fname = ip_name + disk_rname
            pie = Pie(ip, disk_name, value, 'Empty', evalue, fname)
            if ip not in rt_di:
                rt_di[ip] = [pie]
            else:
                rt_di[ip].append(pie)

    return rt_di


# # 服务器增删改查
# # 检验服务器字段
# def check_server_field(request, method):
#     # 检验重复IP
#     server_list = get_serverlist()
#     server_iplist = []
#     for old_server in server_list:
#         server_iplist.append(old_server.get_ip())
#     # 校对字段
#     check_report = {'report': True}
#     if method == "new":
#         server_ip1 = request.POST.get('server_ip1')
#         server_ip2 = request.POST.get('server_ip2')
#         server_ip3 = request.POST.get('server_ip3')
#         server_ip4 = request.POST.get('server_ip4')
#
#         server_ip = str(server_ip1) + "." + str(server_ip2) + "." + str(server_ip3) + "." + str(server_ip4)
#     else:
#         server_ip = request.POST.get('server_ip')
#
#     if request.POST.get('server_detail') == '':
#         server_detail = server_ip
#     else:
#         server_detail = request.POST.get('server_detail')
#
#     if request.POST.get('server_group') == '':
#         server_group = 'test'
#     else:
#         server_group = request.POST.get('server_group')
#
#     server = Server(server_ip, request.POST.get('server_user'), request.POST.get('server_password'),
#                     request.POST.get('server_port'), server_detail,
#                     server_group, request.POST.get('server_state'))
#     # check ip
#     if method == "new":
#         if server_ip in server_iplist:
#             check_report['server_ip'] = "此服务器已存在"
#             check_report['report'] = False
#
#         if server_ip1 == '' or server_ip2 == '' or server_ip3 == '' or server_ip4 == '':
#             check_report['server_ip'] = "IP不可为空"
#             check_report['report'] = False
#
#     # check_server_user
#     if server.get_user() == '':
#         check_report['server_user'] = "服务器用户名不可为空"
#         check_report['report'] = False
#
#     # check_server_user
#     if method == "change":
#         if not check_old_password(server_ip, request.POST.get('server_password_o')):
#             check_report['server_password_o'] = "旧服务密码输入错误"
#             check_report['report'] = False
#
#     if server.get_password() == '':
#         check_report['server_password'] = "密码不能为空"
#         check_report['report'] = False
#
#     if request.POST.get('server_password_t') != server.get_password():
#         check_report['server_password_t'] = "两次输入的密码不同"
#         check_report['report'] = False
#
#     # check_server_port
#     if server.get_port() == '':
#         check_report['server_port'] = "端口号不能为空"
#         check_report['report'] = False
#
#     check_report['server'] = server
#
#     return check_report


# 插入修改server信息
# def insert_server(server):
#     mysql = MysqlDb('mysql-host')
#     server_list = [server.get_ip(), server.get_user(), server.get_password(), int(server.get_port()),
#                    server.get_detail(),
#                    server.get_group(), int(server.get_state())]
#     value_list = [server.get_user(), server.get_password(), int(server.get_port()), server.get_detail(),
#                   server.get_group(),
#                   int(server.get_state())]
#     sql = "insert into server_list values(%s,%s,%s,%s,%s,%s,%s,'1') on duplicate key update user=%s,password=%s,port=%s,detail=%s,`group`=%s,state=%s,servertype='1'"
#     rs_tu = mysql.run_sql(sql, server_list + value_list)
#     if len(rs_tu) == 0:
#         return True
#     else:
#         return False

#
# # 删除指定IP，非删除，将IP备份的备份表中
# def delete_bak_server(server_ip_list):
#     mysql = MysqlDb('mysql-host')
#     ip_list = ''
#     for ip in server_ip_list:
#         ip_list = ip_list + "'" + ip + "',"
#     sql = "insert into server_list_bak SELECT *,now() from server_list where ip in (" + ip_list[:-1] + ")"
#     rs_tu = mysql.run_sql(sql, '')
#     if len(rs_tu) == 0:
#         sql = "delete from server_list where ip in (" + ip_list[:-1] + ")"
#         rs_tu = mysql.run_sql(sql, '')
#         if len(rs_tu) == 0:
#             return True
#         else:
#             return False
#     else:
#         return False


# # 修改指定服务器参数
# def read_server(ip):
#     mysql = MysqlDb('mysql-host')
#     sql = "select * from server_list where ip = %s"
#     rs_tu = mysql.run_sql(sql, ip)
#     rs_li = global_function.tuple_to_list(rs_tu)
#     for li in rs_li:
#         server = Server(li[0], li[1], li[2], li[3], li[4], li[5], li[6])
#
#     return server

#
# def check_old_password(ip, pas):
#     mysql = MysqlDb('mysql-host')
#     sql = "select count(*) from server_list where ip=%s and password=%s"
#     rs_tu = mysql.run_sql(sql, [ip, pas])
#     if rs_tu[0][0] > 0:
#         return True
#     else:
#         return False


# def call_procedure(procedure_name, methon, table_name):
#     mysql = MysqlDb('mysql-host')
#     conn = mysql.get_connect()
#     cur = conn.cursor()
#     if methon == 'new':
#         cur.callproc(procedure_name, (table_name,))
#     else:
#         cur.callproc(procedure_name, (table_name,))
#     data = cur.fetchall()
#     return True


# 获取服务器组内磁盘名称
def get_ip_disk_name_di(group_name):
    mysql = MysqlDb('mysql-host')
    sql = "select distinct(t.disk_name),t.ip FROM statu_disk t left JOIN server_list y ON t.ip=y.ip WHERE t.disk_name <> '' AND  y.GROUP  = %s"
    rs_tu = mysql.run_sql(sql, group_name)
    rs_li = global_function.tuple_to_list(rs_tu)
    ip_disk_name_di = {}
    for li in rs_li:
        if li[1] not in ip_disk_name_di:
            ip_disk_name_di[li[1]] = [li[0]]
        else:
            ip_disk_name_di[li[1]].append(li[0])
    return ip_disk_name_di


# 获取周数的开始日期和结束日期
def get_week_start_end(year, week_num):
    week_di = global_function.get_di_week_time(int(year))
    end_day = ''
    for day in week_di[week_num]:
        if end_day < day:
            end_day = day
    start_day = end_day
    for day in week_di[week_num]:
        if start_day > day:
            start_day = day
    return [start_day[:10], end_day[:10]]
