# _*_ coding: utf-8 _*_

""" FormRequest Object """
from urllib.parse import urlencode

from .request import Request
from base.utils.python import to_bytes, is_listlike


class FormRequest(Request):
    """ Request """

    def __init__(self, *args, **kwargs):
        formdata = kwargs.pop('data', None)
        if formdata and kwargs.get('method') is None:
            kwargs['method'] = 'POST'

        super(FormRequest, self).__init__(*args, **kwargs)

        if formdata:
            items = formdata.items() if isinstance(formdata, dict) else formdata
            querystr = _urlencode(items, self.encoding)
            if self.method == 'POST':
                self.headers.setdefault(b'Content-Type', b'application/x-www-form-urlencoded')
                self._set_data(querystr)
            else:
                self._set_url(self.url + ('&' if '?' in self.url else '?') + querystr)

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


def _urlencode(seq, enc):
    values = [(to_bytes(k, enc), to_bytes(v, enc))
              for k, vs in seq
              for v in (vs if is_listlike(vs) else [vs])]
    return urlencode(values, doseq=1)
