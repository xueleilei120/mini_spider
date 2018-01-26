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
        self.max_retry_count = self.settings.get_int("RETRY_COUNT")
        self.retry_status_codes = self.settings.get_list("RETRY_STATUS_CODES")

    def process_response(self, request, response):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_status_codes:
            return self._retry(request) or response
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, self.RETRY_EXCEPTIONS) \
                and request.meta.get("dont_retry", False):
            return self._retry(request)

    def _retry(self, request):
        retry_count = request.meta.get("retry_count", 0) + 1
        if retry_count <= self.max_retry_count:
            retry_request = request.copy()
            retry_request.meta["retry_count"] = retry_count
            retry_request.dont_filter = True
            return retry_request
