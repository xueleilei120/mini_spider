# _*_ coding: utf-8 _*_
# author : "liuyc"
# date : 2018/1/17 20:20
# desc : "请求尝试次数中间件"

from base.core.downloader.middleware import DownloaderMiddleware


class RetryMiddleware(DownloaderMiddleware):

    """ Retry Middleware """

    RETRY_EXCEPTIONS = ()

    def __init__(self, spider):
        self.spider = spider
        self.settings = spider.settings
        # 尝试次数
        self.max_retry_count = self.settings.get_int("RETRY_COUNT")
        # 需要尝试的状态码
        self.retry_status_codes = self.settings.get_list("RETRY_STATUS_CODES")

    def process_response(self, request, response):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_status_codes:
            return self.__retry(request) or response
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, self.RETRY_EXCEPTIONS) \
                and request.meta.get("dont_retry", False):
            return self.__retry(request)

    def __retry(self, request):
        retry_count = request.meta.get("retry_count", 0) + 1
        if retry_count <= self.max_retry_count:
            retry_request = request.copy()
            retry_request.meta["retry_count"] = retry_count
            retry_request.dont_filter = True
            return retry_request
