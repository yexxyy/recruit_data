# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb.cursors
from twisted.enterprise import adbapi
import redis

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
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        print(item)
        return item

    def open_spider(self, spider):
        print('Pipelines: Sipder is opening')

    def close_spider(self, spider):
        print('Pipelines: Spider has closed')
    
    def handle_error(self,failure,item,spider):
        print(failure)







class ZhilianspiderPipeline(RecruitspiderPipeline):
    def process_item(self, item, spider):
        print(item)
        query=self.dbpool.runInteraction(self.do_insert_company,item)
        query.addErrback(self.handle_error,item,spider)
        return item
    
    
    def do_insert_company(self,cursor,item):
        insert_sql,values=item.zhilian_com_insert_sql()
        cursor.execute(insert_sql,values)
        
