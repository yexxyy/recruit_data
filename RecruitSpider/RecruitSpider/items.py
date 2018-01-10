# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose,Join
import re,hashlib

class BaseItemLoader(ItemLoader):
	default_output_processor = TakeFirst()


def get_null_value(value):
	return value if value else 'NULL'

def remove_blank(value):
	return re.sub(r'\s+','',value)

def get_md5(value):
	print(value)
	if isinstance(value,str):
		value=value.encode('utf-8')
		md5_obj=hashlib.md5()
		md5_obj.update(value)
		return md5_obj.hexdigest()
	
def get_salary_high(value):
	#'8001-10000元/月\xa0',
	m=re.match('(\d+)-(\d+)',value)
	return m.group(2)

def get_salary_low(value):
	m=re.match('(\d+)-(\d+)',value)
	return m.group(1)

def handle_recruit_num(value):
	m=re.match(r"\d+",value)
	if m:
		return m.group(0)
	else:
		return 0

class RecruitspiderItem(scrapy.Item):
	# zhilian_job
	name = scrapy.Field()
	city = scrapy.Field()
	salary_low = scrapy.Field(
		input_processor=MapCompose(get_salary_low)
	)
	salary_high = scrapy.Field(
		input_processor=MapCompose(get_salary_high)
	)
	location = scrapy.Field(
		input_processor=MapCompose(remove_blank)
	)
	publish_date = scrapy.Field()
	label = scrapy.Field()
	nature = scrapy.Field()
	work_years = scrapy.Field()
	education = scrapy.Field()
	recruit_num = scrapy.Field(
		input_processor=MapCompose(handle_recruit_num)
	)
	category = scrapy.Field()
	url = scrapy.Field()
	md5= scrapy.Field(
		input_processor=MapCompose(get_md5)
	)
	content=scrapy.Field(
		input_processor=MapCompose(remove_blank)
	)
	
	# zhilian_company
	com_md5 = scrapy.Field(
		input_processor=MapCompose(get_md5)
	)
	com_name = scrapy.Field()
	com_scale = scrapy.Field()
	com_nature = scrapy.Field()
	com_logo = scrapy.Field(
		input_processor=MapCompose(get_null_value)
	)
	com_website = scrapy.Field(
		input_processor=MapCompose(get_null_value)
	)
	com_industry = scrapy.Field()
	com_address = scrapy.Field(
		input_processor=MapCompose(remove_blank,get_null_value)
	)
	
	created_at = scrapy.Field()
	
	def zhilian_com_insert_sql(self):
		insert_sql = """
			INSERT INTO zhilian_company (
				com_md5,
				com_name,
				com_scale,
				com_nature,
				com_logo,
				com_website,
				com_industry,
				com_address,
				created_at
			) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		values = (
			self['com_md5'],
			self['com_name'],
			self['com_scale'],
			self['com_nature'],
			self['com_logo'],
			self['com_website'],
			self['com_industry'],
			self['com_address'],
			self['created_at']
		)
		return insert_sql, values
	
	def zhilian_job_insert_sql(self):
		insert_sql = """
			INSERT INTO zhilian_job(
				name,
				city,
				com_md5,
				md5,
				salary_low,
				salary_high,
				location,
				publish_date,
				label,
				nature,
				work_years,
				education,
				recruit_num,
				category,
				content,
				created_at,
				url
			) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		values = (
			self['name'],
			self['city'],
			self['com_md5'],
			self['md5'],
			self['salary_low'],
			self['salary_high'],
			self['location'],
			self['publish_date'],
			self['label'],
			self['nature'],
			self['work_years'],
			self['education'],
			self['recruit_num'],
			self['category'],
			self['content'],
			self['created_at'],
			self['url']
		)
		return insert_sql, values