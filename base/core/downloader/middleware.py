# _*_ coding: utf-8 _*_

"""Dowloader Midlleware"""
import logging
from collections import defaultdict

from base.https.request import Request
from base.utils.misc import load_object


class DownloaderMiddleware(object):

    """ DownloaderMiddleware iterface """

    pass


class DownloaderMiddlewareManager(object):

    """ DownloaderMiddlewareManager """

    def __init__(self, spider):
        self.spider = spider
        self.methods = defaultdict(list)
        self.middlewares = self.load_middleware()
        for miw in self.middlewares:
            self._add_middleware(miw)

    def load_middleware(self):
        middlewares = []
        miw_dict = self.spider.settings.get("DOWNLOADER_MIDDLEWARES", {})
        # 按values排序从小到大
        miw_list = sorted(miw_dict.items(), key=lambda x: x[1])
        for miw_path, _ in miw_list:
            cls_miw = load_object(miw_path)
            if issubclass(cls_miw, DownloaderMiddleware):
                obj_miw = cls_miw(self.spider)
                middlewares.append(obj_miw)
            else:
                logging.error("{0} is not DownloaderMiddleware subclass".format(miw_path))
        return middlewares

    def _add_middleware(self, miw):
        if hasattr(miw, "process_request"):
            self.methods["process_request"].append(miw.process_request)
        if hasattr(miw, "process_response"):
            self.methods["process_response"].insert(0, miw.process_response)
        if hasattr(miw, "process_exception"):
            self.methods["process_exception"].insert(0, miw.process_exception)

    def process_request(self, request):
        for method in self.methods["process_request"]:
            method(request)
        return request

    def process_response(self, request, response):
        for method in self.methods["process_response"]:
            response = method(request, response)
            if isinstance(response, Request):
                return response
        return response







