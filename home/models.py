# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.

class Homelist(models.Model):
    homename = models.CharField('操作项', max_length=256)
    homeurl = models.CharField('连接地址', max_length=256)

    nav_display = models.BooleanField('导航显示', default=False)
    home_display = models.BooleanField('首页显示', default=False)

    def __unicode__(self):
        return self.homename

    def get_absolute_url(self):
        return reverse('homepage', args=(self.homeurl,))

    class Meta:
        verbose_name = '首页'
        verbose_name_plural = '首页'
        ordering = ['homename']


