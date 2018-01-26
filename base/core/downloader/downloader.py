# _*_ coding: utf-8 _*_
# 下载器和中间件执行模块
import logging
import asyncio
import aiohttp

from base.https.response import Response
from base.core.downloader.middleware import DownloaderMiddlewareManager


class DownloadHandler(object):

    """ DownloadHandler """

    def __init__(self, spider, **kwargs):
        self.settings = spider.settings
        self.kwargs = kwargs

    async def fetch(self, request):
        try:
            proxy = request.meta.get("proxy")
            kwargs = {
                "headers": request.headers,
                "timeout": self.settings["TIMEOUT"],
            }
            await asyncio.sleep(1)
            if proxy:
                kwargs["proxy"] = proxy
                logging.info("user proxy %s", proxy)
            kwargs.update(self.kwargs)

            url = request.url
            loop = asyncio.get_event_loop()
            async with aiohttp.ClientSession(loop=loop) as session:
                if request.method == "POST":
                    response = await session.post(url, data=request.data, **kwargs)
                else:
                    response = await session.get(url, **kwargs)
                content = await response.read()
                return Response(str(response.url), response.status,
                                response.headers, content)
        except Exception as _e:
            logging.exception(_e)
        return Response(str(request.url), 404)


class Downloader(object):

    """ Downloader """

    def __init__(self, spider):
        self.hanlder = DownloadHandler(spider)
        self.middleware = DownloaderMiddlewareManager(spider)

    async def fetch(self, request):
        """
        request, Request, 请求
        """
        # 请求预处理
        request = self.middleware.process_request(request)
        # 开始请求
        response = await self.hanlder.fetch(request)
        # 返回预处理
        response = self.middleware.process_response(request, response)
        return response
