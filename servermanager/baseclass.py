# -*- coding:utf-8 -*-

class EquipmentIpBelong(object):
    def __init__(self, ip, mac, port, fatherip, level, detail, category):
        self.__ip = ip
        self.__mac = mac
        self.__port = port
        self.__faterip = fatherip
        self.__level = level
        self.__detail = detail
        self.__category = category

    def get_ip(self):
        return self.__ip

    def get_mac(self):
        return self.__mac

    def get_port(self):
        return self.__port

    def get_faterip(self):
        return self.__faterip

    def get_level(self):
        return self.__level

    def get_detail(self):
        return self.__detail

    def get_category(self):
        return self.__category


class ServerIpJtopo(object):
    def __init__(self, ip, color):
        self.__ip = ip
        self.__color = color

    def get_ip(self):
        return self.__ip

    def get_color(self):
        return self.__color


class Server(object):
    def __init__(self, ip, user, password, port, detail, group, state):
        self.__ip = ip
        self.__user = user
        self.__password = password
        self.__port = port
        self.__detail = detail
        self.__group = group
        self.__state = state

    def get_ip(self):
        return self.__ip

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def get_port(self):
        return self.__port

    def get_detail(self):
        return self.__detail

    def get_group(self):
        return self.__group

    def get_state(self):
        return self.__state
