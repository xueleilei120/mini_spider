# _*_ coding: utf-8 _*_

import logging
from parsel import Selector

from base.https.form import FormRequest
from base.core.spider import Spider
from base.xmongodb.mongodb_client import MongodbClientX


class CFCSpider(Spider):
    """ 中国基金中心数据抓取 """
    start_urls = [
        "http://blog.jobbole.com/all-posts/",
    ]
    heardes = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept': '*/*',
        'Content-Length': '123',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://data.foundationcenter.org.cn/foundation.html',
        'Origin': 'http://data.foundationcenter.org.cn',
        'Host': 'data.foundationcenter.org.cn',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self):
        super(CFCSpider, self).__init__("CFCSpider")
        self.mongodb_client = MongodbClientX(self.settings, collection_name="cfc")

    def parse(self, response):
        post_url = "http://data.foundationcenter.org.cn/NewFTI/GetFDOPagedFoundation.ashx"
        request_data = {
            "keyWord": "",
            "pageIndex": "1",
            "pageSize": "25",
            "type": "2",
            "sqlWhere": "",
            "sqlTop": "",
            "flag": "0",
            "financeField": "%u51C0%u8D44%u4EA7",
            "searchMode": "0",
            "biaoji": ""
        }
        yield FormRequest(url=post_url, data=request_data, headers=self.heardes,
                          callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = None
        try:
            print(response.body[:100])
        except Exception as _e:
            logging.exception(_e)
        return item

    def process_item(self, item):
        logging.debug("push item: {0}".format(str(item)))
        self.mongodb_client.process_item(item)
