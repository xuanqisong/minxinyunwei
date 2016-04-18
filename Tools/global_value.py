# -*- coding:utf-8 -*-
# 密码加密KEY key 1023     -1024
ENCRYPT_KEY_VALUE = 1
# 文件管理权限set
# HOME_FILE_MANAGER_PERMISSIONS = (['home_backupfiledir_download', 'home_backupfiledir_upload', 'home_backupfiledir_show'
#                                   'home_linuxdownloadfiledir_download', 'home_linuxdownloadfiledir_download',
#                                   'home_linuxdownloadfiledir_show'
#                                   'home_uploadfiledir_download', 'home_uploadfiledir_upload',
#                                   'home_uploadfiledir_show'])
HOME_FILE_SHOW_PERMISSIONS = (['backupfiledir', 'linuxdownloadfiledir', 'uploadfiledir'])
HOME_FILE_SHOW_DICT = {'backupfiledir': '备份文件', 'linuxdownloadfiledir': '服务器下载文件', 'uploadfiledir': '上传文件'}
