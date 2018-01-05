# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb.cursors
from twisted.enterprise import adbapi


class RecruitspiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        print('Come on baby,the sipder is opening')

    def close_spider(self, spider):
        print('Spider has closed')
    
        






class ZhilianspiderPipeline(RecruitspiderPipeline):
    def process_item(self, item, spider):
        return item
    
    
    