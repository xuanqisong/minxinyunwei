"""minxinyunwei URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # login_nopower_logout
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^no_power/$', 'django.contrib.auth.views.login', {'template_name': 'mismatch_power.html'}),

    # console
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'home.views.index', name='index'),
    url(r'^homepage/(?P<values>[^/]+)/$', 'home.views.test', name='homepage'),

    # ajax

    url(r'^navigation_host/', 'home.views.ajax_index', name='ajax_navigation'),


]
# monitor
urlpatterns += [
    # monitor
    url(r'^homepage/monitor/index/', 'monitor.views.index', name='monitorindex'),
    # monitor configuration

    # monitor ztcx
    url(r'^homepage/monitor/ztcxindex/', 'monitor.views.ztcxindex', name='status_ip_ztcxindex'),
    url(r'^homepage/monitor/status_ip/', 'monitor.views.status_ip', name='status_ip'),
    # monitor rbbb
    url(r'^homepage/monitor/rbbb', 'monitor.views.rbbbindex', name='rbbb_rbbbindex'),
    url(r'^homepage/monitor/data/', 'monitor.views.rbbbdata', name='rbbb_rbbbdata'),
    # monitor_zbbb
    url(r'^homepage/monitor/zbbb', 'monitor.views.zbbbindex', name='zbbb_zbbbindex'),
    url(r'^homepage/monitor/zbdata/', 'monitor.views.zbbbdata', name='rbbb_zbbbdata'),
    # monitor fwqpz
    # url(r'^homepage/monitor/configuration/', 'monitor.views.fwpz', name='fwpz'),
    # url(r'^monitor/templates/new_server/', 'monitor.views.newserver_mid', name='fwpz_newserver_mid'),
    # url(r'^homepage/monitor/newserver/', 'monitor.views.newserver', name='fwpz_newserver'),
    # url(r'^homepage/monitor/change_server/', 'monitor.views.changeserver_mid', name='fwpz_changeserver_mid'),
    # url(r'^homepage/monitor/changeserver/', 'monitor.views.changeserver', name='fwpz_changeserver'),
    # url(r'^homepage/monitor/deleteserver/', 'monitor.views.deleteserver', name='fwpz_deleteserver'),

    # ajax
    url(r'^homepage/monitor/ajaxgroup_diskname/', 'monitor.views.ajax_group_disk_name', name='ajax_group_disk_name'),
]
# script
urlpatterns += [
    # script
    url(r'^homepage/script/', 'script.views.index', name='script'),
    # url(r'^script/sshmanager/', 'script.views.sshmanager', name='sshmanager'),
    url(r'^script/showservergroup/', 'script.views.showservergroup', name='script_show_server_group'),
    url(r'^script/getconnectserverip/', 'script.views.base_view', name='script_getconnectserverip'),
    # websocket
    url(r'^script/a$', 'script.views.base_view', name='script_websocket_runshell'),
    url(r'^script/runshell$', 'script.views.start_shell', name='script_websocket_runshell'),

    # script_fwpz
    # url(r'^script/new_server/', 'script.views.newserver_mid', name='script_fwpz_newserver_mid'),
    # url(r'^script/newserver/', 'script.views.newserver', name='script_fwpz_newserver'),
    # url(r'^script/change_server/', 'script.views.changeserver_mid', name='script_fwpz_changeserver_mid'),
    # url(r'^script/changeserver/', 'script.views.changeserver', name='script_fwpz_changeserver'),
    # url(r'^script/deleteserver/', 'script.views.deleteserver', name='script_fwpz_deleteserver'),

    # script_file_manager
    url(r'^script/filemanager/', 'script.views.file_manager', name='script_file_manager'),
    url(r'^script/uploadfile/', 'script.views.uploadfile', name='script_uploadfile'),
    url(r'^script/servicefilemanager/', 'script.views.downloadfile', name='script_downloadfile'),

    # ajax
    url(r'^script/ajax/getserverdetail/', 'script.views.ajax_server_detail', name='script_ajax_server_detail'),
    url(r'^script/ajax/filemanager/', 'script.views.ajax_file_detail', name='script_ajax_file_detail'),
]
# antivirus
urlpatterns += [
    # antivirus
    url(r'^homepage/antivirus/index/', 'antivirus.views.index', name='antivirus'),
    url(r'^antivirus/once/', 'antivirus.views.mid_onec_antivirus', name='antiviurs_once_configuration'),
    url(r'^antivirus/manualcheck/', 'antivirus.views.manual_check', name='antivirus_manual_check'),

    # websocket
    url(r'^antivirus/antivirusmanualstart$', 'antivirus.views.start_clamdav', name='antivirus_run'),
    # ajax
    url(r'^antivirus/getserverip/', 'antivirus.views.get_server_ipname', name='antivirus_group_serverip'),
]

# servermanager
urlpatterns += [
    # servermanager
    # url(r'^servermanager$','servermanager.views.index',name='servermanagertest'),
    # url(r'^homepage/servermanager/routermanager', 'servermanager.views.routermanager',
    #     name='servermanager_routermanager'),
    url(r'^homepage/servermanager/index', 'servermanager.views.index', name='servermanagertest'),
    url(r'^homepage/servermanager/showserverused', 'servermanager.views.showserverused', name='showserverused'),
    # servermanager_fwpz
    # url(r'^servermanager/templates/new_server/', 'servermanager.views.newserver_mid',
    #     name='servermanager_fwpz_newserver_mid'),
    # url(r'^homepage/servermanager/newserver/', 'servermanager.views.newserver', name='servermanager_fwpz_newserver'),
    # url(r'^homepage/servermanager/change_server/', 'servermanager.views.changeserver_mid',
    #     name='servermanager_fwpz_changeserver_mid'),
    # url(r'^homepage/servermanager/changeserver/', 'servermanager.views.changeserver',
    #     name='servermanager_fwpz_changeserver'),
    # url(r'^homepage/servermanager/deleteserver/', 'servermanager.views.deleteserver',
    #     name='servermanager_fwpz_deleteserver'),
    # servermanager_bakrouterfile
    url(r'^servermanager/routerfilebak/', 'servermanager.views.showbakfile', name='servernamager_showbakfile'),
    url(r'^servermanager/download/routerfilebak/', 'servermanager.views.downloadbakfile',
        name='servermanager_downloadbakfile'),

    # ajax
    url(r'^servermanager/detailbakfile/', 'servermanager.views.ajaxdetailbakfile',
        name='ajax_servermanagerdetailbakfile'),
]
# home
urlpatterns += [
    # job
    url(r'^sysconfiguration/job/', 'home.views.configuration_job', name='home_configuration_job'),
    url(r'^sysconfiguration/insertjobmessage/', 'home.views.insert_jobmessage', name='home_insert_jobmessage'),
    # job ajax
    url(r'^sysconfiguration/ajax/jobfiledetail', 'home.views.ajax_configuration_job',
        name='home_ajax_configuration_job'),
    url(r'^sysconfiguration/ajax/changerunmark', 'home.views.ajax_change_run_mark', name='home_change_run_mark'),
    url(r'^sysconfiguration/ajax/deletejob', 'home.views.ajax_delete_job', name='home_delete_job'),

    # server manager
    url(r'^sysconfiguration/servermanager/', 'home.views.fwqpz', name='home_fwqpz'),
    url(r'^sysconfiguration/newservermid/', 'home.views.new_server_mid', name='home_new_server_mid'),
    url(r'^sysconfiguration/newserver/', 'home.views.newserver', name='home_new_server'),
    url(r'^sysconfiguration/changeservermid/', 'home.views.change_service_mid', name='home_change_service_mid'),
    url(r'^sysconfiguration/changeserver/', 'home.views.change_service', name='home_change_server'),
    url(r'^sysconfiguration/deleteserver/', 'home.views.delete_server', name='home_delete_server'),

    # file manager
    url(r'^sysconfiguration/filedetail/', 'home.views.file_detail', name='home_file_detail'),
    # file manager ajax
    url(r'^sysconfiguration/ajax/filedetail/', 'home.views.ajax_file_attribute', name='home_file_attribute'),
]
# static files
import os
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    media_root = os.path.join(settings.BASE_DIR, 'templates')
    urlpatterns += static('/templates/', document_root=media_root)
