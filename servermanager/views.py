# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
import use_factions

import os


@login_required(login_url='/login/')
def index(request):
    return render(request, 'servermanagerindex.html', {})


# 查看使用情况
@user_passes_test(lambda u: u.has_perm('servermanager.Use'), login_url='/no_power/')
def showserverused(request):
    di = {}
    # 获取IP段
    server_ip_section_li = use_factions.get_ipsection()
    # 获取IP段内IP
    ipsection_ip_di = use_factions.get_ipinsectionip(server_ip_section_li)
    # 获取ServerIpJtopo列表
    ipsection_serveripjtopo_di = use_factions.get_serveripjtopolist(ipsection_ip_di)
    di['ipsection_serveripjtopo_di'] = ipsection_serveripjtopo_di
    return render(request, 'showserverused.html', di)


# # 路由器配置
# @user_passes_test(lambda u: u.has_perm('servermanager.Show'), login_url='/no_power/')
# def routermanager(request, di={}):
#     server_list = use_factions.get_serverlist()
#
#     di['server_list'] = server_list
#     return render(request, 'servermanagerfwpz.html', di)


# def newserver_mid(request):
#     di = {}
#     server_group = []
#     for group in use_factions.get_server_grouplist():
#         server_group.append(group[0])
#     di['server_groupa'] = server_group
#     return render(request, 'servermanagernew_server.html', di)


# @user_passes_test(lambda u: u.has_perm('servermanager.New'), login_url='/no_power/')
# def newserver(request):
#     check_report = use_factions.check_server_field(request, "new")
#     if check_report['report']:
#         if use_factions.insert_server(check_report['server']):
#             use_factions.call_procedure('new_partition', 'new', 'statu_cpu')
#             use_factions.call_procedure('new_partition', 'new', 'statu_disk')
#             use_factions.call_procedure('new_partition', 'new', 'statu_memory')
#             check_report['alert'] = '<Script Language="JavaScript"> alert("服务器存储成功"); </Script>'
#         else:
#             check_report['alert'] = '<Script Language="JavaScript"> alert("服务器存储失败"); </Script>'
#         return routermanager(request, check_report)
#     else:
#         return render(request, 'servermanagernew_server.html', check_report)


# @user_passes_test(lambda u: u.has_perm('servermanager.Change'), login_url='/no_power/')
# def changeserver_mid(request, di={}):
#     server_ip = request.POST.getlist('server_ip')
#     if len(server_ip) == 0:
#         di['alert'] = '<Script Language="JavaScript"> alert("请选择要修改服务器"); </Script>'
#         return routermanager(request, di)
#     elif len(server_ip) > 1:
#         di['alert'] = '<Script Language="JavaScript"> alert("请选择一个服务器"); </Script>'
#         return routermanager(request, di)
#     else:
#         di['server'] = use_factions.read_server(server_ip[0])
#         return render(request, 'servermanagerchange_server.html', di)


# def changeserver(request):
#     check_report = use_factions.check_server_field(request, "change")
#     if check_report['report']:
#         if use_factions.insert_server(check_report['server']):
#             check_report['alert'] = '<Script Language="JavaScript"> alert("服务器更新成功"); </Script>'
#         else:
#             check_report['alert'] = '<Script Language="JavaScript"> alert("服务器更新失败"); </Script>'
#         return routermanager(request, check_report)
#     else:
#         return render(request, 'servermanagerchange_server.html', check_report)


# @user_passes_test(lambda u: u.has_perm('servermanager.Delete'), login_url='/no_power/')
# def deleteserver(request):
#     di = {}
#     server_ip = request.POST.getlist('server_ip')
#     if len(server_ip) == 0:
#         di['alert'] = '<Script Language="JavaScript"> alert("请选择要删除的服务器"); </Script>'
#         return routermanager(request, di)
#     else:
#         if use_factions.delete_bak_server(server_ip):
#             use_factions.call_procedure('delete_partition', 'delete', 'statu_cpu')
#             use_factions.call_procedure('delete_partition', 'delete', 'statu_disk')
#             use_factions.call_procedure('delete_partition', 'delete', 'statu_memory')
#             di['alert'] = '<Script Language="JavaScript"> alert("服务器删除成功"); </Script>'
#         else:
#             di['alert'] = '<Script Language="JavaScript"> alert("服务器删除失败"); </Script>'
#         return routermanager(request, di)


# 路由备份文件查看
# 展示首页
@user_passes_test(lambda u: u.has_perm('servermanager.Show'), login_url='/no_power/')
def showbakfile(request):
    di = {'data': use_factions.get_file_data()}
    # 获取文件序列
    return render(request, 'routerbakfileindex.html', di)


# 下载备份文件
def downloadbakfile(request):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_path = request.POST.get('fpath')

    the_file_name = dir_name + '\\' + 'routerbakfile\\' + file_path.replace('/', '\\')
    file_name = file_path.replace('/', '\\')[:-1]

    # 获取文件迭代
    yield_bit = use_factions.file_iterator(the_file_name)

    response = StreamingHttpResponse(yield_bit)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)

    return response


# ajax
def ajaxdetailbakfile(request):
    f_dir_name = request.GET['f_dir_name']
    c_file_name = request.GET['c_file_name']
    bakfiledetail = use_factions.get_bakfile_detail(f_dir_name, c_file_name)
    di = {'bakfiledetail': bakfiledetail}
    return JsonResponse(di)
