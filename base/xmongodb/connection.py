# _*_ coding: utf-8 _*_
# author : "666"
# date : 2018/1/24 18:52
# desc : "描述"
import pymongo


def get_mongodb_from_settings(settings):
    params = settings.get_dict('MONGODB_PARAMS')
    client = pymongo.MongoClient(**params)
    return client


# Backwards compatible alias.
from_settings = get_mongodb_from_settings
