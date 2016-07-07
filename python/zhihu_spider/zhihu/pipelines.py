# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from zhihu.items import ZhihuUser

import json

class ZhihuPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonPipeline(object):

    def __init__(self):
        self.zh_user_file =open('data/zh_user.json', 'wb')
        self.zh_user_file.write('[\n')

    def process_item(self, item, spider):
        if  isinstance(item, ZhihuUser):
            self.zh_user_file.write(json.dumps(dict(item), ensure_ascii=False).encode('utf8') + ',\n')
        return item

    def spider_closed(self, spider):
        self.zh_user_file.write('{}\n]')
        self.zh_user_file.close()

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.Connection("localhost", 27017)
        self.db = connection["zhihu"]
        self.user_col = self.db["user"]

    def saveOrUpdate(self,collection,item):
        _id= dict(item).get("_id")
        if _id is not None:
            tmp=collection.find_one({"_id":_id})
            #不存在
            if tmp is None:
                collection.insert(dict(item))
            #只插入不更新
            # else:
            #     collection.update({"_id":_id},dict(item))
        else:
            collection.insert(dict(item))

    def process_item(self, item, spider):
        if isinstance(item, ZhihuUser):
            self.saveOrUpdate(self.user_col, item)
        return item
