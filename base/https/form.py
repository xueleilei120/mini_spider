# _*_ coding: utf-8 _*_

from urllib.parse import urlencode

from .request import Request
from base.utils.python import to_bytes, is_listlike


class FormRequest(Request):
    """ Request post"""

    def __init__(self, *args, **kwargs):
        formdata = kwargs.pop('data', None)
        if formdata and kwargs.get('method') is None:
            kwargs['method'] = 'POST'

        super(FormRequest, self).__init__(*args, **kwargs)

        if formdata:
            querystr = _urlencode(formdata.items(), self.encoding) if isinstance(formdata, dict) else formdata
            if self.method == 'POST':
                self._set_data(querystr)
            else:
                self._set_url(self.url + ('&' if '?' in self.url else '?') + querystr)

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)

    __repr__ = __str__


def _urlencode(seq, enc):
    values = [(to_bytes(k, enc), to_bytes(v, enc)) for k, vs in seq for v in (vs if is_listlike(vs) else [vs])]
    return urlencode(values, doseq=1)
