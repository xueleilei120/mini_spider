# _*_ coding: utf-8 _*_
# author : "666"
# date : 2018/1/12 10:02
# desc : "程序入口"
from spiders.jobbole_spider import JobboleSpider
from spiders.cfc_spider import CFCSpider

if __name__ == "__main__":
    jobbole_spider = JobboleSpider()
    jobbole_spider.start()
    # cfc_spider = CFCSpider()
    # cfc_spider.start()

