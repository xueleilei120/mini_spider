# _*_ coding: utf-8 _*_
# author : "liuyc"
# date : 2018/1/22 16:52
# desc : "描述" 
from .connection import from_settings


class MongodbClientX(object):
    def __init__(self, settings, db_name=None, collection_name=None):
        if db_name is None:
            db_name = "local"
        if collection_name is None:
            collection_name = "local_collection"
        client = from_settings(settings)
        db = client[db_name]
        self.collection = db[collection_name]

    def process_item(self, item):
        self.collection.insert_one(item)
        return item
