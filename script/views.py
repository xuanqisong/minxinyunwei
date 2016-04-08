# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.template import RequestContext
from dwebsocket.decorators import accept_websocket
from django.contrib.auth.decorators import user_passes_test, login_required
import use_factions


@login_required(login_url="/login/")
def index(request):
    return render(request, 'scriptindex.html', {})


# SSH服务器配置
@user_passes_test(lambda u: u.has_perm('script.Show'), login_url='/no_power/')
def sshmanager(request, di={}):
    server_list = use_factions.get_serverlist()

    di['server_list'] = server_list
    return render(request, 'scriptfwpz.html', di)


def newserver_mid(request):
    di = {}
    server_group = []
    for group in use_factions.get_server_grouplist():
        server_group.append(group[0])
    di['server_groupa'] = server_group
    return render(request, 'scriptnew_server.html', di)


@user_passes_test(lambda u: u.has_perm('script.New'), login_url='/no_power/')
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
        return sshmanager(request, check_report)
    else:
        return render(request, 'scriptnew_server.html', check_report)


@user_passes_test(lambda u: u.has_perm('script.Change'), login_url='/no_power/')
def changeserver_mid(request, di={}):
    server_ip = request.POST.getlist('server_ip')
    if len(server_ip) == 0:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择要修改服务器"); </Script>'
        return sshmanager(request, di)
    elif len(server_ip) > 1:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择一个服务器"); </Script>'
        return sshmanager(request, di)
    else:
        di['server'] = use_factions.read_server(server_ip[0])
        return render(request, 'scriptchange_server.html', di)


def changeserver(request):
    check_report = use_factions.check_server_field(request, "change")
    if check_report['report']:
        if use_factions.insert_server(check_report['server']):
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器更新成功"); </Script>'
        else:
            check_report['alert'] = '<Script Language="JavaScript"> alert("服务器更新失败"); </Script>'
        return sshmanager(request, check_report)
    else:
        return render(request, 'scriptchange_server.html', check_report)


@user_passes_test(lambda u: u.has_perm('script.Delete'), login_url='/no_power/')
def deleteserver(request):
    di = {}
    server_ip = request.POST.getlist('server_ip')
    if len(server_ip) == 0:
        di['alert'] = '<Script Language="JavaScript"> alert("请选择要删除的服务器"); </Script>'
        return sshmanager(request, di)
    else:
        if use_factions.delete_bak_server(server_ip):
            use_factions.call_procedure('delete_partition', 'delete', 'statu_cpu')
            use_factions.call_procedure('delete_partition', 'delete', 'statu_disk')
            use_factions.call_procedure('delete_partition', 'delete', 'statu_memory')
            di['alert'] = '<Script Language="JavaScript"> alert("服务器删除成功"); </Script>'
        else:
            di['alert'] = '<Script Language="JavaScript"> alert("服务器删除失败"); </Script>'
        return sshmanager(request, di)


# 选择连接连接组
@user_passes_test(lambda u: u.has_perm('script.Show'), login_url='/no_power/')
def showservergroup(request):
    servergourplist = use_factions.get_server_grouplist()
    di = {'servergrouplist': [servergourplist[0][0], servergourplist[1][0]]}
    return render(request, 'script_selectgroup.html', di)


# 确定连接服务器
def getconnectserverip(request):
    connect_serverip = request.POST.getlist('connect_ip')

    di = use_factions.get_websshbase(connect_serverip)
    di['serverip_list'] = connect_serverip
    base_view(request, di)


# ajax
def ajax_server_detail(request):
    group_name = request.GET['name']
    di = use_factions.get_group_server_detail(group_name)
    return JsonResponse(di)


# websocket
webssh_server_list = []


@user_passes_test(lambda u: u.has_perm('script.Use'), login_url='/no_power/')
def base_view(request):
    connect_serverip = request.POST.getlist('connect_ip')
    user = request.user

    di = use_factions.get_websshbase(connect_serverip)
    for k, v in di.items():
        for c in v:
            if c not in webssh_server_list:
                webssh_server_list.append(c)

    di['serverip_list'] = connect_serverip
    di['file_name_list'] = use_factions.get_file_name_list(request)
    di['user'] = str(user)
    return render_to_response('script_webssh.html', di, context_instance=RequestContext(request))


clients = []


@accept_websocket
def start_shell(request):
    if request.is_websocket:
        try:
            clients.append(request.websocket)
            for message in request.websocket:
                if not message:
                    break
                try:
                    # for a in use_factions.detection_message(message, webssh_server_list, clients):
                    #     webssh_server_list.remove(a)
                    print message
                    li = use_factions.detection_message(message, webssh_server_list, clients)
                    for l in li:
                        webssh_server_list.remove(l)
                except Exception as e:
                    print "main", e

        finally:
            clients.remove(request.websocket)


# uploadfile for file manager
def uploadfile(request):
    if use_factions.save_file(request):
        return file_manager(request, {'alert': 'uploadfile success'})
    else:
        return file_manager(request, {'alert': 'uploadfile faile'})


# downloadfile for file manager
def downloadfile(request):
    response = StreamingHttpResponse(use_factions.downloadfile(request))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(request.POST.get('file_name'))
    return response


# file_manager
@login_required(login_url="/login/")
def file_manager(request, di={}):
    di['data'] = use_factions.get_downloadfile(request)
    return render(request, 'downloadfilemanager.html', di)


# ajax
def ajax_file_detail(request):
    file_name = request.GET['file_name']
    di = use_factions.get_file_detail(file_name, request)
    return JsonResponse(di)
