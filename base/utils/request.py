# _*_ coding: utf-8 _*_

""" 工具 """

import hashlib
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode


def request_fingerprint(request):
    """request fingerprint
    """
    scheme, netloc, path, params, query, fragment = urlparse(request.url)
    keyvals = parse_qsl(query)
    keyvals.sort()
    query = urlencode(keyvals)
    canonicalize_url = urlunparse((
        scheme, netloc.lower(), path, params, query, fragment))
    fpr = hashlib.sha1()
    fpr.update(canonicalize_url.encode("utf-8"))
    return fpr.hexdigest()





