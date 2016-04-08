# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from home.models import Homelist


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
