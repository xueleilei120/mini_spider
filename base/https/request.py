# _*_ coding: utf-8 _*_

""" Request Object """
from w3lib.url import safe_url_string
from base.utils.python import to_bytes


class Request(object):

    """ Request """

    def __init__(self, url, method='GET', callback=None,
                 errback=None, headers=None, encoding='utf-8', data=None, dont_filter=False, meta=None):
        self.encoding = encoding  # this one has to be set first
        self._set_url(url)
        self.method = method.upper()
        self.callback = callback
        self.errback = errback
        self.headers = headers or {}
        self._data = data
        self.dont_filter = dont_filter
        self.meta = meta if meta else {}

    def copy(self, *args, **kwargs):
        """ copy """
        for key in ["url", "method", "callback", "headers", "meta"]:
            kwargs.setdefault(key, getattr(self, key))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    def _get_url(self):
        return self._url

    def _set_url(self, url):
        if not isinstance(url, str):
            raise TypeError('Request url must be str or unicode, got %s:' % type(url).__name__)

        self._url = safe_url_string(url, self.encoding)

        if ':' not in self._url:
            raise ValueError('Missing scheme in request url: %s' % self._url)

    url = property(_get_url, _set_url, )

    def _get_data(self):
        return self._data

    def _set_data(self, data):
        if data is None:
            self._data = b''
        else:
            self._data = to_bytes(data, self.encoding)

    data = property(_get_data, _set_data)

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)

    __repr__ = __str__
