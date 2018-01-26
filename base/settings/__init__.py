# _*_ coding: utf-8 _*_

""" 配置管理类：Settings """

import json

from importlib import import_module

from . import settings


class Attribute(object):

    """ Attribute Object """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "<Attribute value=%s>" % self.value

    __repr__ = __str__


class Settings(object):

    """ Settings Object """

    def __init__(self, values=None):
        self.attrs = {}
        self.load_config(settings)
        if values is not None:
            self.set_dict(values)

    def __getitem__(self, key):
        """
        :param key: str
        """
        return self.attrs[key].value if key in self.attrs else None

    def load_config(self, module):
        """
        :param module: module
        """
        if isinstance(module, str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def set(self, key, value):
        """
        :param key:
        :param value: int/float/str
        """
        self.attrs[key] = Attribute(value)

    def set_dict(self, values):
        """
        :param values: dict
        :return:
        """
        for key, value in values.items():
            self.set(key, value)

    def get(self, key, default=None):
        """
        :param key:str
        :param default:
        :return:
        """
        return self[key] or default

    def get_int(self, key, default=0):
        """
        :param key: str
        :param default: int
        :return:
        """
        return int(self.get(key, default))

    def get_float(self, key, default=0.0):
        """
        :param key: str
        :param default: float
        :return:
        """
        return float(self.get(key, default))

    def get_list(self, key, default=None):
        """
        :param key: str
        :param default: list
        :return:
        """
        value = self.get(key, default or None)
        if isinstance(value, str):
            value = value.split(",")
        return value

    def get_dict(self, key, default=None):
        """
        :param key: str
        :param default: dict
        :return:
        """
        value = self.get(key, default or None)
        if isinstance(value, str):
            value = json.loads(value)
        return value
