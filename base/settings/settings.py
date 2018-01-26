# _*_ coding: utf-8 _*_

""" 一些默认配置"""

# 是否为调试模式
DEBUG = True

RETRY_COUNT = 3

RETRY_STATUS_CODES = [500, 502, 503, 504, 400, 403, 408]

TIMEOUT = 10

DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
}

PROXY_ENABLED = False

MAX_REQUEST_SIZE = 30

PROXY_FILE = "proxy_list.txt"
PROXY_INTERVAL = 5

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    # "base.downloadermiddlewares.proxy.ProxyMiddleware": 200,
    "base.downloadermiddlewares.encode.EncodingDiscriminateMiddleware": 100,
    "base.downloadermiddlewares.retry.RetryMiddleware": 300,
    "base.downloadermiddlewares.useragent.UserAgentMiddleware": 400,
}

# 同时允许任务数量
TASK_LIMIT = 5

######################### redis配置 #########################
REDIS_PARAMS = {
    'host': "118.190.209.166",
    'port': 6379,
    'password': "root",
}
######################### mongodb配置 #########################
MONGODB_PARAMS = {
    'host': "118.190.209.166",
    'port': 27017,
}