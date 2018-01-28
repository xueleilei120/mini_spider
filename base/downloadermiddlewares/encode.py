# _*_ coding: utf-8 _*_
# author : "666"
# date : 2018/1/17 20:16
# desc : "自动识别response编码"

import chardet
from urllib.parse import urlparse

from base.core.downloader.middleware import DownloaderMiddleware


class EncodingDiscriminateMiddleware(DownloaderMiddleware):

    """ Encoding Discriminate Middleware """

    ENCODING_MAP = {}

    def __init__(self, spider):
        self.spider = spider

    def process_response(self, request, response):
        netloc = urlparse(request.url).netloc
        content = response.body
        if self.ENCODING_MAP.get(netloc) is None:
            # 自动识别编码
            encoding = chardet.detect(content)["encoding"]
            encoding = "GB18030" \
                if encoding.upper() in ("GBK", "GB2312") else encoding
            self.ENCODING_MAP[netloc] = encoding
        body = content.decode(self.ENCODING_MAP[netloc], "replace")
        return response.copy(body=body)