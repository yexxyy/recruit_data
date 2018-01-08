# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitspiderItem(scrapy.Item):
	# zhilian_job
	name = scrapy.Field()
	city = scrapy.Field()
	salary_low = scrapy.Field()
	salary_high = scrapy.Field()
	location = scrapy.Field()
	publish_date = scrapy.Field()
	label = scrapy.Field()
	nature = scrapy.Field()
	work_years = scrapy.Field()
	education = scrapy.Field()
	recruit_num = scrapy.Field()
	category = scrapy.Field()
	url = scrapy.Field()
	
	# zhilian_company
	com_md5 = scrapy.Field()
	com_name = scrapy.Field()
	com_scale = scrapy.Field()
	com_nature = scrapy.Field()
	com_logo = scrapy.Field()
	com_website = scrapy.Field()
	com_industry = scrapy.Field()
	com_address = scrapy.Field()
	
	created_at= scrapy.Field()