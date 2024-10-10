# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo.errors import DuplicateKeyError

class MongoPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
        mongo_uri = crawler.settings["MONGO_URI"],
        mongo_db  = crawler.settings["MONGO_DB"],
        )

    def __init__(self, mongo_uri, mongo_db):
        self.uri = pymongo.MongoClient(mongo_uri)
        self.db  = self.uri[mongo_db]

    def process_item(self, item, spider):
        """
        考虑到不同collection的划分，在item内使用coll字段进行标记
        :param item:
        :param spider:
        :return:
        """
        coll = "novels"
        item['_id'] = item['id']
        try:
            self.db[coll].insert_one(item)
        except DuplicateKeyError:       # 考虑到了history需要不断更新记录，所以使用update而不用insert
            self.db[coll].update_one({"_id": item.get("_id")}, {"$set": item}, upsert=True)
        return item
