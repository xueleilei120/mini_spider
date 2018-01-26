#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liuyc
@file: redisclient.py
@time: 2017/11/3 22:55
@describe:
"""


import redis
redis_client = redis.Redis(host="118.190.209.166", port=6379, db=0, password="root", )


if __name__ == "__main__":
    redis_client.ping()
    redis_client.set("a", "1")
    print(redis_client.get("a"))