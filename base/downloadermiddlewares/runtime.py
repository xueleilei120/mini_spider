# _*_ coding: utf-8 _*_
# author : "liuyc"
# date : 2018/1/27 20:25
# desc : "在请求时检查是否为正确运行时间"

import logging
import time
from datetime import datetime

from base.core.downloader.middleware import DownloaderMiddleware


class CheckRunTime(DownloaderMiddleware):

    """ CheckRunTime Middleware """

    def __init__(self, spider):
        self.spider = spider
        self.settings = spider.settings
        # 可以运行的时间
        self.run_time = self.settings.get_dict("RUN_TIME")
        # 是否可以运行
        self.is_run = True

    def can_run(self):
        is_run = True
        now = datetime.now()
        dct = {
            "day": now.day,
            "week": now.weekday(),
            "hour": now.hour,
            "minute": now.minute,
        }
        for k, v in self.run_time.items():
            if len(v) == 2:
                _min = v[0]
                _max = v[1]
                if dct[k] < _min or dct[k] > _max:
                    is_run = False
                    logging.warning("---> Not in running time: {0}:{1} <---".format(k, v))
                    break
        return is_run

    def process_request(self, request):
        while not self.can_run():
            time.sleep(5)

        return request



