#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<yeli.studio@qq.com> on 2018/1/5 14:58

from sqlalchemy import create_engine
from RecruitSpider import settings
import hashlib



def get_city_pinyin():
	import pinyin
	sql_str = "SELECT name FROM city WHERE parent_id <> 0"
	cities_pinyin = []
	for item in execute_sql(sql_str):
		cities_pinyin.append(pinyin.get(item, format='strip'))
	cities_pinyin.remove('zhongqing')
	cities_pinyin.append('chongqing')
	return cities_pinyin


def get_job_url_md5():
	sql_str="SELECT url FROM zhilian_job"
	result=execute_sql(sql_str)
	processed_result=[]
	for item in result:
		processed_result.append(get_md5(item))
	return processed_result

def execute_sql(sql_str):
	engine = create_engine('mysql://{}:{}@{}:3306/{}?charset=utf8'.format(settings.MYSQL_USER,settings.MYSQL_PASSWORD,settings.MYSQL_HOST,settings.MYSQL_DBNAME), echo=False)
	conn = engine.connect()
	result = conn.execute(sql_str)
	result = result.fetchall()
	conn.close()
	processed_result = []
	for item in result:
		processed_result.append(item[0])
	return processed_result


def get_md5(value):
	if isinstance(value,str):
		value=value.encode('utf-8')
		md5_obj=hashlib.md5()
		md5_obj.update(value)
		return md5_obj.hexdigest()
