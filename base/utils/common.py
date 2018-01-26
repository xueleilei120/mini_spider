# _*_ coding: utf-8 _*_

""" 公共工具 """

import six


def result2list(result):
    """ result to result"""
    if result is None:
        return []
    if isinstance(result, (dict, str)):
        return [result]
    if hasattr(result, "__iter__"):
        return result


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s
