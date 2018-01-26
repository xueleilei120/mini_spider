# _*_ coding: utf-8 _*_

""" Base Spider"""
import logging

from base.settings import Settings
from base.https.request import Request
from base.core.engine import Engine
from base.utils.logger import init_logger


class Spider(object):

    custom_settings = None

    def __init__(self, name="base_spider"):
        if not hasattr(self, "start_urls"):
            self.start_urls = []
        self.name = name
        # init settings
        self.settings = Settings(self.custom_settings)
        init_logger(self.settings, self.name)
        self.initialize()

    def initialize(self):
        pass

    def start_requests(self):
        logging.info("---------------> %s: start <---------------" % self.name)
        logging.info("---------------> start_urls=%s <---------------" % self.start_urls)
        for url in self.start_urls:
            yield Request(url, dont_filter=True)

    def start(self):
        engine = Engine(self)
        engine.start()

    def parse(self, response):
        raise NotImplementedError

    def process_item(self, item):
        pass
