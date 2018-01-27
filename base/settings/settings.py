# _*_ coding: utf-8 _*_

""" 一些默认配置"""

# 是否为调试模式
DEBUG = True

# 尝试次数
RETRY_COUNT = 3
# 需尝试的状态码
RETRY_STATUS_CODES = [500, 502, 503, 504, 400, 403, 408]

# 请求最大延迟时间
TIMEOUT = 10


PROXY_FILE = "proxy_list.txt"
# 每个代理使用间隔
PROXY_INTERVAL = 1

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    # "base.downloadermiddlewares.proxy.ProxyMiddleware": 200,
    "base.downloadermiddlewares.encode.EncodingDiscriminateMiddleware": 100,
    # "base.downloadermiddlewares.retry.RetryMiddleware": 300,
    "base.downloadermiddlewares.useragent.UserAgentMiddleware": 400,
    "base.downloadermiddlewares.runtime.CheckRunTime": 500,
}

# 同时允许任务数量
TASK_LIMIT = 5

RUN_TIME = {"day": (1, 31), "week": (0, 6), "hour": (0, 23), "minute": (0, 59)}

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