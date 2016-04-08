# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse

import use_factions


# index
# @user_passes_test(lambda u: u.has_perm('monitor.use'), login_url='/login/')
@login_required(login_url='/login/')
def index(request):
    return render(request, 'monitorindex.html', {})


# ztcx
@login_required(login_url='/login/')
def ztcxindex(request):
    di = {}

    servernamelist = use_factions.get_serverlist()
    [start_time, end_time] = use_factions.get_startendtime()
    di['servernamelist'] = servernamelist
    di['startt'] = start_time
    di['endt'] = end_time
    return render(request, 'monitorztcx.html', di)


@user_passes_test(lambda u: u.has_perm('monitor.Use'), login_url='/no_power/')
def status_ip(request):
    ip = [request.POST.get('server_ip')]
    start_time = request.POST.get('starttime')
    end_time = request.POST.get('endtime')
    picture_quxiantu_list = []
    ip_list = use_factions.get_server_ip(ip)

    di = {}
    cpu_quxiantu_list = use_factions.make_quxiantu_data_startend(ip_list, "CPU", start_time, end_time)
    memory_quxiantu_list = use_factions.make_quxiantu_data_startend(ip_list, "MEMORY", start_time, end_time)

    picture_quxiantu_list.append(cpu_quxiantu_list)
    picture_quxiantu_list.append(memory_quxiantu_list)

    di['picture_quxiantu_list'] = picture_quxiantu_list

    return render(request, 'picture.html', di)


# rbbb
@user_passes_test(lambda u: u.has_perm('monitor.Use'), login_url='/no_power/')
def rbbbindex(request):
    di = {}
    server_grouplist = []

    listfather = use_factions.get_server_grouplist()
    monitor_day_list = use_factions.get_monitor_day_list()
    for li in listfather:
        server_grouplist.append(li[0])
    di['server_grouplist'] = server_grouplist
    di['monitor_day_list'] = monitor_day_list
    return render(request, 'monitorrbbb.html', di)


def rbbbdata(request):
    di = {}
    picture_quxiantu_list = []
    picture_zhuzhuangtu_list = []
    group_name = request.POST.get('group_name')
    monitor_day_year = request.POST.get('monitor_day_year')
    monitor_day_mounth = request.POST.get('monitor_day_mounth')
    monitor_day_day = request.POST.get('monitor_day_day')

    monitor_time_list = use_factions.get_monitor_time_list()
    monitor_day = monitor_day_year + "-" + monitor_day_mounth + "-" + monitor_day_day
    if monitor_day not in monitor_time_list:
        di['method'] = 'no_data'
        return render(request, 'no_date.html', di)

    total = request.POST.get('total')
    ip_disk_name = request.POST.getlist('ip_disk_name')

    ip_disk_name_di = {}
    for value in ip_disk_name:
        ip_disk_name_list = value.split('@')
        if ip_disk_name_list[0] not in ip_disk_name_di:
            ip_disk_name_di[ip_disk_name_list[0]] = [ip_disk_name_list[1]]
        else:
            ip_disk_name_di[ip_disk_name_list[0]].append(ip_disk_name_list[1])

    server_ip_list = use_factions.get_group_ip_list(group_name)

    cpu_quxiantu_list = use_factions.make_quxiantu_data(server_ip_list, "CPU", monitor_day)
    memory_quxiantu_list = use_factions.make_quxiantu_data(server_ip_list, "MEMORY", monitor_day)
    # disk_zhuzhuangtu_list = use_factions.make_zhuzhuangtu_data(server_ip_list, "DISK", monitor_day)
    zhuzhuangtugroupfather = use_factions.make_zhuzhuangtu_group_date(server_ip_list, monitor_day, ip_disk_name_di)
    # pie_di = use_factions.get_pie_date(server_ip_list, monitor_day, ip_disk_name_di)

    # 获取图表Y轴上下标


    if total == 'a':
        combine_cpu_quxiantu = [use_factions.combine_show(cpu_quxiantu_list)]
        combine_memory_quxiantu = [use_factions.combine_show(memory_quxiantu_list)]
        picture_quxiantu_list.append(combine_cpu_quxiantu)
        picture_quxiantu_list.append(combine_memory_quxiantu)

    else:
        picture_quxiantu_list.append(cpu_quxiantu_list)
        picture_quxiantu_list.append(memory_quxiantu_list)

    # picture_zhuzhuangtu_list.append(disk_zhuzhuangtu_list)
    di['picture_zhuzhuangtu_list'] = picture_zhuzhuangtu_list
    di['picture_quxiantu_list'] = picture_quxiantu_list
    di['group_name'] = group_name
    di['zhuzhuangtugroupfather'] = zhuzhuangtugroupfather
    # di['pie_di'] = pie_di

    return render(request, 'rbbb_picture.html', di)


# zbbb
@user_passes_test(lambda u: u.has_perm('monitor.Use'), login_url='/no_power/')
def zbbbindex(request):
    di = {}
    server_grouplist = []

    listfather = use_factions.get_server_grouplist()
    for li in listfather:
        server_grouplist.append(li[0])
    di['server_grouplist'] = server_grouplist
    return render(request, 'monitorzbbb.html', di)


def zbbbdata(request):
    week_time = request.POST.get('weektime')
    week_num = week_time[-2:]
    year = week_time[:4]
    week_start, week_end = use_factions.get_week_start_end(year, week_num)

    di = {}
    picture_quxiantu_list = []
    picture_zhuzhuangtu_list = []
    group_name = request.POST.get('group_name')
    total = request.POST.get('total')
    ip_disk_name = request.POST.getlist('ip_disk_name')

    ip_disk_name_di = {}
    for value in ip_disk_name:
        ip_disk_name_list = value.split('@')
        if ip_disk_name_list[0] not in ip_disk_name_di:
            ip_disk_name_di[ip_disk_name_list[0]] = [ip_disk_name_list[1]]
        else:
            ip_disk_name_di[ip_disk_name_list[0]].append(ip_disk_name_list[1])

    server_ip_list = use_factions.get_group_ip_list(group_name)

    cpu_quxiantu_list = use_factions.make_quxiantu_data_startend(server_ip_list, "CPU", week_start, week_end)
    memory_quxiantu_list = use_factions.make_quxiantu_data_startend(server_ip_list, "MEMORY", week_start, week_end)
    zhuzhuangtugroupfather = use_factions.make_zhuzhuangtu_group_date(server_ip_list, week_end, ip_disk_name_di)

    # 获取图表Y轴上下标

    if total == 'a':
        combine_cpu_quxiantu = [use_factions.combine_show(cpu_quxiantu_list)]
        combine_memory_quxiantu = [use_factions.combine_show(memory_quxiantu_list)]
        picture_quxiantu_list.append(combine_cpu_quxiantu)
        picture_quxiantu_list.append(combine_memory_quxiantu)

    else:
        picture_quxiantu_list.append(cpu_quxiantu_list)
        picture_quxiantu_list.append(memory_quxiantu_list)

    di['picture_zhuzhuangtu_list'] = picture_zhuzhuangtu_list
    di['picture_quxiantu_list'] = picture_quxiantu_list
    di['group_name'] = group_name
    di['zhuzhuangtugroupfather'] = zhuzhuangtugroupfather

    return render(request, 'rbbb_picture.html', di)


# fwpz
@user_passes_test(lambda u: u.has_perm('monitor.Show'), login_url='/no_power/')
def fwpz(request, di={}):
    server_list = use_factions.get_serverlist()

    di['server_list'] = server_list
    return render(request, 'monitorfwpz.html', di)


def newserver_mid(request):
    di = {}
    server_group = []
    for group in use_factions.get_server_grouplist():
        server_group.append(group[0])
    di['server_groupa'] = server_group
    return render(request, 'new_server.html', di)


@user_passes_test(lambda u: u.has_perm('monitor.New'), login_url='/no_power/')
def newserver(request):
    check_report = use_factions.check_server_field(request, "new")
    if check_report['report']:
        if use_factions.insert_server(check_report['server']):
            use_factions.call_procedure('new_partition', 'new', 'statu_cpu')
            use_factions.call_procedure('new_partition', 'new', 'statu_disk')
            use_factions.call_procedure('new_partition', 'new', 'statu_memory')
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器存储成功"); </Script>'
        else:
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器存储失败"); </Script>'
        return fwpz(request, check_report)
    else:
        return render(request, 'new_server.html', check_report)


def changeserver_mid(request, di={}):
    server_ip = request.POST.getlist('server_ip')
    if len(server_ip) == 0:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择要修改服务器"); </Script>'
        return fwpz(request, di)
    elif len(server_ip) > 1:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择一个服务器"); </Script>'
        return fwpz(request, di)
    else:
        di['server'] = use_factions.read_server(server_ip[0])
        return render(request, 'change_server.html', di)


@user_passes_test(lambda u: u.has_perm('monitor.Change'), login_url='/no_power/')
def changeserver(request):
    check_report = use_factions.check_server_field(request, "change")
    if check_report['report']:
        if use_factions.insert_server(check_report['server']):
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器更新成功"); </Script>'
        else:
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器更新失败"); </Script>'
        return fwpz(request, check_report)
    else:
        return render(request, 'change_server.html', check_report)


@user_passes_test(lambda u: u.has_perm('monitor.Delete'), login_url='/no_power/')
def deleteserver(request):
    di = {}
    server_ip = request.POST.getlist('server_ip')
    if len(server_ip) == 0:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择要删除的服务器"); </Script>'
        return fwpz(request, di)
    else:
        if use_factions.delete_bak_server(server_ip):
            use_factions.call_procedure('delete_partition', 'delete', 'statu_cpu')
            use_factions.call_procedure('delete_partition', 'delete', 'statu_disk')
            use_factions.call_procedure('delete_partition', 'delete', 'statu_memory')
            di['alert'] = '<Script Language="JavaScript"> alert("服务器删除成功"); </Script>'
        else:
            di['alert'] = '<Script Language="JavaScript"> alert("服务器删除失败"); </Script>'
        return fwpz(request, di)


# ajax
def ajax_group_disk_name(request):
    group_name = request.GET['name']
    di = use_factions.get_ip_disk_name_di(group_name)
    return JsonResponse(di)
