# _*_ coding: utf-8 _*_

import logging
from parsel import Selector

from base.https.request import Request
from base.core.spider import Spider
from base.xmongodb.mongodb_client import MongodbClientX


class TestSpider(Spider):
    """ TestSpider """
    start_urls = [
        "http://blog.jobbole.com/all-posts/",
        # "http://tool.chinaz.com/Tools/",
    ]

    def __init__(self):
        super(TestSpider, self).__init__("TestSpider")
        self.mongodb_client = MongodbClientX(self.settings, collection_name="jobbole")

    def parse(self, response):
        select = Selector(response.body)
        next_url = select.xpath("//a[@class='next page-numbers']/@href").extract_first()
        if next_url:
            logging.info("next page url:%s" % next_url)
            yield Request(next_url, callback=self.parse, dont_filter=True)
        urls = select.xpath("//a[@class='archive-title']/@href")
        for url in urls:
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = None
        try:
            logging.debug(response.url)
            select = Selector(response.body)
            title = select.xpath("//div[@class='entry-header']/h1/text()").extract_first()
            if title:
                item = {"title": title, "url": response.url}
        except Exception as _e:
            logging.exception(_e)
        return item

    def process_item(self, item):
        logging.debug("push item: {0}".format(str(item)))
        self.mongodb_client.process_item(item)
