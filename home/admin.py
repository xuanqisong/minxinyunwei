# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Homelist

class HomelistAdmin(admin.ModelAdmin):
	list_display = ('homename','homeurl','nav_display','home_display')
# Register your models here.



admin.site.register(Homelist,HomelistAdmin)
# Register your models here.