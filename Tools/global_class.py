class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst


class Singleton2(type):
    def __init__(cls, name, bases, dict):
        super(Singleton2, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton2, cls).__call__(*args, **kw)
        return cls._instance


class Server(object):
    def __init__(self, value_list):
        self.value_list = value_list
        self.ip = ''
        self.user = ''
        self.password = ''
        self.port = ''
        self.detail = ''
        self.group = ''
        self.status = ''
        self.servertype = ''

    def binding_server_value(self):
        self.ip = self.value_list[0]
        self.user = self.value_list[1]
        self.password = self.value_list[2]
        self.port = self.value_list[3]
        self.detail = self.value_list[4]
        self.group = self.value_list[5]
        self.status = self.value_list[6]
        self.servertype = self.value_list[7]
