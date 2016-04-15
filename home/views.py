# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from home.models import Homelist
import use_factions


# 首页
def index(request):
    di = {}
    home_display_columns = Homelist.objects.filter(home_display=True)
    di['home_display_columns'] = home_display_columns
    return render(request, 'index.html', di)


def test(request, values):
    return HttpResponse('homepage:   ' + values)


def ajax_index(request):
    di = {}
    group_name = request.GET['name']
    home_display_columns = Homelist.objects.filter(home_display=True)

    for homelist in home_display_columns:
        di[homelist.homename] = homelist.get_absolute_url()
    return JsonResponse(di)


class UrlName(object):
    def __init__(self, name, url):
        self.__name = name
        self.__url = url

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url


# job
def configuration_job(request, di=None):
    if di is None:
        di = {}
    di['data'] = use_factions.get_file_data()
    di['job_detail'] = use_factions.job_message()
    return render(request, 'job_configuration.html', di)


def insert_jobmessage(request):
    function_name = request.POST.get('function_name')
    year_n = request.POST.get('year_t')
    month_n = request.POST.get('month_t')
    day_n = request.POST.get('day_t')
    hour_n = request.POST.get('hour_t')
    minute_n = request.POST.get('minute_t')
    second_n = request.POST.get('second_t')
    if use_factions.insert_jobmessage(function_name, year_n, month_n, day_n, hour_n, minute_n, second_n):
        di = {'alert': "存储成功"}
    else:
        di = {'alert': "存储失败"}
    di['data'] = use_factions.get_file_data()
    return render(request, 'job_configuration.html', di)


# job ajax
def ajax_configuration_job(request):
    f_dir_name = request.GET['f_dir_name']
    return JsonResponse(use_factions.get_job_detail(f_dir_name))


def ajax_change_run_mark(request):
    pid = request.GET['id']
    run_mark = request.GET['run_mark']
    li = use_factions.change_run_mark(pid, run_mark)
    if li[0]:
        return JsonResponse({'id': pid, 'run_mark': li[1]})
    else:
        return JsonResponse({'id': pid, 'run_mark': li[1]})


def ajax_delete_job(request):
    pid = request.GET['id']
    if use_factions.delete_job(pid):
        return JsonResponse({'id': pid})
    else:
        return JsonResponse({'id': 'false'})


# service manager
def fwqpz(request, di={}):
    di['server_list'] = use_factions.service_detail()
    return render(request, 'fwqpz.html', di)


def new_server_mid(request):
    di = {'service_group': use_factions.service_group()}
    return render(request, 'fwq_new.html', di)


def newserver(request):
    check_report = use_factions.check_server_field(request, "new")
    # 读取需要加分区的表
    status_table_list = use_factions.get_status_table()
    if check_report['report']:
        if use_factions.insert_server(check_report['server']):
            for tu in status_table_list:
                use_factions.call_procedure('new_partition', 'new', tu[0])
            # use_factions.call_procedure('new_partition', 'new', 'statu_cpu')
            # use_factions.call_procedure('new_partition', 'new', 'statu_disk')
            # use_factions.call_procedure('new_partition', 'new', 'statu_memory')
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器存储成功"); </Script>'
        else:
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器存储失败"); </Script>'
        return fwqpz(request, check_report)
    else:
        return render(request, 'new_server.html', check_report)


def change_service_mid(request):
    di = {}
    server_ip = request.POST.getlist('server_ip')
    if len(server_ip) == 0:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择要修改服务器"); </Script>'
        return fwqpz(request, di)
    elif len(server_ip) > 1:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择一个服务器"); </Script>'
        return fwqpz(request, di)
    else:
        di['server'] = use_factions.read_service(server_ip[0])
        return render(request, 'fwq_change.html', di)


def change_service(request):
    check_report = use_factions.check_server_field(request, "change")
    if check_report['report']:
        if use_factions.insert_server(check_report['server']):
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器更新成功"); </Script>'
        else:
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器更新失败"); </Script>'
        return fwqpz(request, check_report)
    else:
        return render(request, 'fwq_change.html', check_report)


def delete_server(request):
    di = {}
    server_ip = request.POST.getlist('server_ip')
    status_table_list = use_factions.get_status_table()
    if len(server_ip) == 0:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择要删除的服务器"); </Script>'
        return fwqpz(request, di)
    else:
        if use_factions.delete_bak_server(server_ip):
            for tu in status_table_list:
                use_factions.call_procedure('delete_partition', 'delete', tu[0])
            # use_factions.call_procedure('delete_partition', 'delete', 'statu_cpu')
            # use_factions.call_procedure('delete_partition', 'delete', 'statu_disk')
            # use_factions.call_procedure('delete_partition', 'delete', 'statu_memory')
            di['alert'] = '<Script Language="JavaScript"> alert("服务器删除成功"); </Script>'
        else:
            di['alert'] = '<Script Language="JavaScript"> alert("服务器删除失败"); </Script>'
        return fwqpz(request, di)
