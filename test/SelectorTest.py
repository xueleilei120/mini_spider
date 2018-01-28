# _*_ coding: utf-8 _*_
# author : "liuyc"
# date : 2018/1/28 16:59
# desc : "描述"


class SelectTest(object):
    def __init__(self):
        self._cached_selector = None

    @property
    def selector(self):
        if self._cached_selector is None:
            pass
        return self._cached_selector

    def xpath(self, query, **kwargs):
        return self.selector.xpath(query, **kwargs)

    def css(self, query):
        return self.selector.css(query)

if __name__ == "__main__":
    cls_select = SelectTest()
    cls_select.xpath("")

