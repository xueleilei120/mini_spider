# _*_ coding: utf-8 _*_

import logging
from lxml import etree

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
        html = etree.HTML(response.body)
        next_page = html.xpath("//a[@class='next page-numbers']/@href")
        if next_page:
            next_url = next_page[0]
            logging.info("next page url:%s" % next_url)
            yield Request(next_url, callback=self.parse, dont_filter=True)
        urls = html.xpath("//a[@class='archive-title']/@href")
        for url in urls:
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = None
        try:
            logging.debug(response.url)
            html = etree.HTML(response.body)
            title_list = html.xpath("//div[@class='entry-header']/h1/text()")
            if title_list:
                title = title_list[0].strip()
                item = {"title": title, "url": response.url}
        except Exception as _e:
            logging.exception(_e)
        return item

    def process_item(self, item):
        logging.debug("push item: {0}".format(str(item)))
        self.mongodb_client.process_item(item)
