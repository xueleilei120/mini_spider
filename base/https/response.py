# _*_ coding: utf-8 _*_

""" Response Object """


class Response(object):

    """ Response """

    def __init__(self, url, status=200, headers=None, body='', request=None):
        self.url = url
        self.status = status
        self.headers = headers or {}
        self.body = body
        self.request = request
        self._cached_selector = None

    def copy(self, *args, **kwargs):
        for key in ["url", "status", "headers", "body", "request"]:
            kwargs.setdefault(key, getattr(self, key))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    def __str__(self):
        return "<%d %s>" % (self.status, self.url)

    __repr__ = __str__

    @property
    def selector(self):
        from parsel import Selector
        if self._cached_selector is None:
            self._cached_selector = Selector(self.body)
        return self._cached_selector

    def xpath(self, query, **kwargs):
        return self.selector.xpath(query, **kwargs)

    def css(self, query):
        return self.selector.css(query)
