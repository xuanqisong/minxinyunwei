# -*- coding: utf-8 -*-
from django.shortcuts import render
from antivirus.baseclass import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required

import use_factions

from django.shortcuts import render_to_response
from django.template import RequestContext
from dwebsocket.decorators import accept_websocket


# index
@login_required(login_url="/login/")
def index(request):
    return render(request, 'antivirusindex.html', {})


# def once_check(request):
#     re_di = use_factions.one_times('10.255.12.233', 'multiscan_file', '/monitor_python/')
#     return HttpResponse(re_di)

@user_passes_test(lambda u: u.has_perm('monitor.Use'), login_url="/no_power/")
def mid_onec_antivirus(request):
    di = {}
    server_grouplist = []
    for li in use_factions.get_server_group():
        server_grouplist.append(li[0])

    di['server_grouplist'] = server_grouplist
    return render(request, 'antivirusmanual.html', di)


clamavlist = []


def manual_check(request):
    di = {}

    dir_hole_name = request.POST.getlist('dir_hole_name')
    if len(dir_hole_name) == 0:
        return render(request, 'antivirusmanual.html', {'alert': '请选择服务器'})
    scan_type = request.POST.get('scan_type')
    ip_dir_di = use_factions.get_ip_dir(dir_hole_name)
    for ip, dir_namelist in ip_dir_di.items():
        for dir_name in dir_namelist:
            clamav = ClamAV(ip, scan_type, dir_name)
            clamavlist.append(clamav)

    html_show_list = []
    for ip, dir_name_list in ip_dir_di.items():
        for dir_name in dir_name_list:
            html_show_list.append(RunStatuHtml(ip, dir_name, str(ip).replace('.', '') + str(dir_name).replace('/', '')))

    di['scan_type'] = scan_type
    di['ip_dir_di'] = ip_dir_di
    di['ip_dir_diforhtml'] = html_show_list
    return render_to_response('antivirusmanualrun.html', di, context_instance=RequestContext(request))


# ajax
def get_server_ipname(request):
    group_name = request.GET['group_name']
    serveriplist = []
    for li in use_factions.get_group_serveripname(group_name):
        serveriplist.append(li[0])

    di = {'serveriplist': serveriplist}
    return JsonResponse(di)


# websocket
clients = []
whilecheckclamavrun = WhileCheckClamavRun()


@accept_websocket
def start_clamdav(request):
    if request.is_websocket:
        try:
            clients.append(request.websocket)
            for message in request.websocket:
                if not message:
                    break
                for client in clients:
                    print message
                    if message == "start":
                        whilecheckclamavrun.message = message
                        whilecheckclamavrun.get_clamavlist(clamavlist)
                        whilecheckclamavrun.client = client
                        whilecheckclamavrun.start()

                        check_thread_list = []
                        for clamav in clamavlist:
                            check_thread_list.append(clamav)

                        for clamav in check_thread_list:
                            clamavlist.remove(clamav)

                    elif message == "stop":
                        whilecheckclamavrun.message = message
                        if not whilecheckclamavrun.is_alive():
                            whilecheckclamavrun.message = None
                            whilecheckclamavrun.get_clamavlist([])
                            whilecheckclamavrun.client = None

        finally:
            clients.remove(request.websocket)


# # job
# def configuration_job(request, di={}):
#     di['data'] = use_factions.get_file_data()
#     di['job_detail'] = use_factions.job_detail()
#     return render(request, 'job_configuration.html', di)
#
#
# def insert_jobmessage(request):
#     function_name = request.POST.get('function_name')
#     year_n = request.POST.get('year_n')
#     month_n = request.POST.get('month_n')
#     day_n = request.POST.get('day_n')
#     hour_n = request.POST.get('hour_n')
#     minute_n = request.POST.get('minute_n')
#     second_n = request.POST.get('second_n')
#     if use_factions.insert_jobmessage(function_name, year_n, month_n, day_n, hour_n, minute_n, second_n):
#         di = {'alert': "存储成功"}
#     else:
#         di = {'alert': "存储失败"}
#     di['data'] = use_factions.get_file_data()
#     return render(request, 'job_configuration.html', di)
#
#
# # job ajax
# def ajax_configuration_job(request):
#     f_dir_name = request.GET['f_dir_name']
#     return JsonResponse(use_factions.get_job_detail(f_dir_name))


