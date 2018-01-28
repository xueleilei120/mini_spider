# _*_ coding: utf-8 _*_

import logging

from base.https.request import Request
from base.core.spider import Spider
from base.xmongodb.mongodb_client import MongodbClientX


class JobboleSpider(Spider):
    """ JobboleSpider """
    start_urls = [
        "http://blog.jobbole.com/all-posts/",
    ]

    def __init__(self):
        super(JobboleSpider, self).__init__("JobboleSpider")
        self.mongodb_client = MongodbClientX(self.settings, collection_name="jobbole")

    def parse(self, response):
        next_url = response.xpath("//a[@class='next page-numbers']/@href").extract_first()
        if next_url:
            logging.info("next page url:%s" % next_url)
            yield Request(next_url, callback=self.parse, dont_filter=True)
        urls = response.xpath("//a[@class='archive-title']/@href").extract()
        for url in urls:
            yield Request(url.strip(), callback=self.parse_detail)

    def parse_detail(self, response):
        item = None
        try:
            logging.debug(response.url)
            title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first()
            if title:
                item = {"title": title, "url": response.url}
        except Exception as _e:
            logging.exception(_e)
        return item

    def process_item(self, item):
        logging.debug("push item: {0}".format(str(item)))
        self.mongodb_client.process_item(item)
