# _*_ coding: utf-8 _*_
# author : "liuyc"
# date : 2018/1/12 10:02
# desc : "程序入口"
from parsel import Selector
from spiders.test_spider import TestSpider

if __name__ == "__main__":
    cls_spider = TestSpider()
    cls_spider.start()
