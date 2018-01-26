# _*_ coding: utf-8 _*_
# author : "liuyc"
# date : 2018/1/17 20:10
# desc : "代理中间件"

import random
import logging
import time

from base.core.downloader.middleware import DownloaderMiddleware

PROXY_LIST = [
    "",
]


class ProxyMiddleware(DownloaderMiddleware):

    """ Proxy Middleware """

    def __init__(self, spider):
        self.spider = spider
        self.settings = spider.settings
        self.host_time_map = {}
        self.proxy_interval = self.settings["PROXY_INTERVAL"]
        self.proxy_file = self.settings["PROXY_FILE"]
        self.proxy_list = PROXY_LIST
        # with open(self.proxy_file) as fip:
        #     self.proxy_list = fip.readlines()

    def process_request(self, request):
        request.meta["proxy"] = self._get_proxy()

    def _get_proxy(self):
        proxy = random.choice(self.proxy_list).strip()
        latest = self.host_time_map.get(proxy, 0)
        interval = time.time() - latest
        if interval < self.proxy_interval:
            logging.info("%s waitting ...", proxy)
            time.sleep(self.proxy_interval)
        self.host_time_map[proxy] = time.time()
        return proxy

