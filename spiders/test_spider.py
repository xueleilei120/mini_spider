# _*_ coding: utf-8 _*_

import logging
from parsel import Selector

from base.https.request import Request
from base.https.form import FormRequest
from base.core.spider import Spider
from base.xmongodb.mongodb_client import MongodbClientX


class TestSpider(Spider):
    """ TestSpider """
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
        super(TestSpider, self).__init__("TestSpider")
        self.mongodb_client = MongodbClientX(self.settings, collection_name="jobbole")

    """
    POST http://data.foundationcenter.org.cn/NewFTI/GetFDOPagedFoundation.ashx HTTP/1.1
    Host: data.foundationcenter.org.cn
    Connection: keep-alive
    Content-Length: 123
    Accept: */*
    Origin: http://data.foundationcenter.org.cn
    X-Requested-With: XMLHttpRequest
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
    Content-Type: application/x-www-form-urlencoded
    Referer: http://data.foundationcenter.org.cn/foundation.html
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9
    Cookie: Hm_lvt_efb83c40fc1d14e53093543cee57a13d=1512124603,1512617324,1513047420; recordcontent=%7B%27%u4E2D%u56FD%u5987%u5973%u53D1%u5C55%u57FA%u91D1%u4F1A%27%3A%5B%27113%27%2C%27412379207.28%27%5D%2C%27%u5B89%u5FBD%u5987%u5973%u513F%u7AE5%u53D1%u5C55%u57FA%u91D1%u4F1A%27%3A%5B%27728504%27%2C%27%27%5D%2C%27%u5B89%u5FBD%u7701%u5F90%u60B2%u9E3F%u6559%u80B2%u57FA%u91D1%u4F1A%27%3A%5B%27170%27%2C%27%27%5D%2C%27%u6DF1%u5733%u58F9%u57FA%u91D1%u516C%u76CA%u57FA%u91D1%u4F1A%27%3A%5B%272142%27%2C%27370921590.83%27%5D%2C%27%u6DF1%u5733%u5E02%u7231%u4F51%u672A%u6765%u6148%u5584%u57FA%u91D1%u4F1A%27%3A%5B%276126%27%2C%270%27%5D%2C%27%20%u6DF1%u5733%u5E02%u660E%u56ED%u6148%u5584%u57FA%u91D1%u4F1A%27%3A%5B%27728612%27%2C%27%27%5D%2C%27%u4E1C%u839E%u5E02%u6F6E%u6C55%u5546%u4F1A%u6148%u5584%u57FA%u91D1%u4F1A%27%3A%5B%274835%27%2C%271946329.64%27%5D%2C%27%u5B81%u590F%u51CF%u707E%u6276%u8D2B%u57FA%u91D1%u4F1A%27%3A%5B%27727932%27%2C%27%27%5D%2C%27%u978D%u5C71%u5E02%u89C1%u4E49%u52C7%u4E3A%u57FA%u91D1%u4F1A%27%3A%5B%274057%27%2C%273734071.63%27%5D%2C%27%u6DF1%u5733%u5E02%u56FD%u9645%u4EA4%u6D41%u5408%u4F5C%u57FA%u91D1%u4F1A%27%3A%5B%274472%27%2C%2756265847.63%27%5D%7D; Hm_lvt_1863a16825816064bf2c703f97e54de6=1513255814,1514273176,1514430118,1514430873; mbox=check#true#1516964037|session#1516963976086-368527#1516965837; ASP.NET_SessionId=nybz1zdgpvzf5gdg54wzhauv

    keyWord=&pageIndex=1&pageSize=25&type=2&sqlWhere=&sqlTop=&flag=0&financeField=%25u51C0%25u8D44%25u4EA7&searchMode=0&biaoji=
    """

    def parse(self, response):
        post_url = "http://data.foundationcenter.org.cn/NewFTI/GetFDOPagedFoundation.ashx"
        request_data = "keyWord=&pageIndex=1&pageSize=25&type=2&sqlWhere=&sqlTop=&flag=0&financeField=%25u51C0%25u8D44%25u4EA7&searchMode=0&biaoji="
        yield FormRequest(url=post_url, data=request_data, headers=self.heardes, callback=self.parse_detail)
        # select = Selector(response.body)
        # next_url = select.xpath("//a[@class='next page-numbers']/@href").extract_first()
        # if next_url:
        #     logging.info("next page url:%s" % next_url)
        #     yield Request(next_url, callback=self.parse, dont_filter=True)
        # urls = select.xpath("//a[@class='archive-title']/@href").extract()
        # for url in urls:
        #     yield Request(url.strip(), callback=self.parse_detail)

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
