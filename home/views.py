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
