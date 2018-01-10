#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue on 2017/12/29


import scrapy
from scrapy.http import Request
from scrapy import signals
from scrapy.exceptions import CloseSpider
from RecruitSpider.tools import tool
from urllib.parse import urlparse
from urllib import parse as urllib_parse
from RecruitSpider.items import *
import time

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allow_domains = ['jobs.zhaopin.com']
    base_url = 'http://jobs.zhaopin.com'
    # start_urls = ['http://jobs.zhaopin.com/']

    custom_settings = {
        # 'JOBDIR':'/Users/yexianyong/Desktop/spider/job_dir/zhilian'
        
    }
    cities = tool.get_city_pinyin()
    current_city_index = 0
    current_page = 1

    # 爬虫信号绑定
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ZhilianSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_close, signals.spider_closed)
        crawler.signals.connect(spider.spider_open, signals.spider_opened)
        return spider

    def spider_close(self):
        print('爬虫已关闭')

    def spider_open(self):
        print('爬虫已开始')


    def start_requests(self):
        start_url = urllib_parse.urljoin(self.base_url,
                                         self.cities[self.current_city_index] + ('/p{}/'.format(self.current_page)))
        yield Request(url=start_url, callback=self.parse)

    def parse(self, response):
        print(response)
        parse_obj=urlparse(response.url)
        path_list=parse_obj.path.split('/')
        self.current_city_index=self.cities.index(path_list[1])
        self.current_page=int(path_list[2][1:])
        # 当前城市已完毕，下一个城市
        if self.current_page == 100:
            self.current_page = 1
            self.current_city_index += 1
            if self.current_city_index < len(self.cities):
                temp_url = urllib_parse.urljoin(self.base_url,
                                                self.cities[self.current_city_index] + ('/p{}/'.format(self.current_page)))
                yield Request(url=temp_url, callback=self.parse)
        else:
            self.current_page += 1
            temp_url = urllib_parse.urljoin(self.base_url,
                                            self.cities[self.current_city_index] + ('/p{}/'.format(self.current_page)))
            yield Request(url=temp_url, callback=self.parse)
        # raise CloseSpider(reason='智联爬取完毕...')
        #解析list
        job_list=response.xpath("//ul[contains(@class,'search_list')]/li/div[contains(@class,'details_container')]")
        for job_node in job_list:
            job_url=job_node.xpath("span[@class='post']/a/@href").extract_first()
            yield Request(url=job_url, callback=self.parse_job_detail)

    


    def parse_job_detail(self,response):
        print(response)
        from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # zhilian_job
        item_loader=BaseItemLoader(item=RecruitspiderItem(),response=response)
        name=response.xpath("//div[@class='top-fixed-box']/div/div/h1/text()").extract_first()
        item_loader.add_value('name',name)
        label=response.xpath("//div[@class='top-fixed-box']//div[@class='welfare-tab-box']/span/text()").extract()
        item_loader.add_value('label',','.join(label) if label else "NULL")
        item_loader.add_xpath('salary_low',"//ul/li/span[text()='职位月薪：']/following-sibling::*/text()")
        item_loader.add_xpath('salary_high',"//ul/li/span[text()='职位月薪：']/following-sibling::*/text()")
        item_loader.add_xpath('city',"//ul/li/span[text()='工作地点：']/following-sibling::*/a/text()")
        publist_date=response.xpath("//ul/li/span[text()='发布日期：']/following-sibling::*/span/text()").extract_first()
        item_loader.add_value('publish_date',publist_date)
        item_loader.add_xpath('nature',"//ul/li/span[text()='工作性质：']/following-sibling::*/text()")
        item_loader.add_xpath('work_years',"//ul/li/span[text()='工作经验：']/following-sibling::*/text()")
        item_loader.add_xpath('education',"//ul/li/span[text()='最低学历：']/following-sibling::*/text()")
        item_loader.add_xpath('recruit_num',"//ul/li/span[text()='招聘人数：']/following-sibling::*/text()")
        item_loader.add_xpath('category',"//ul/li/span[text()='职位类别：']/following-sibling::*/a/text()")
        item_loader.add_value('url',response.url)
        content=response.xpath("//div[@class='tab-inner-cont']/p/text()").extract()
        item_loader.add_value('content',','.join(content))
        item_loader.add_xpath('location',"//div[@class='tab-inner-cont']/b[text()='工作地址：']/following-sibling::*/text()")
        
        
        # zhilian_company
        com_logo=response.xpath("//div[@class='company-box']/p[@class='img-border']/a/img/@src").extract_first()
        item_loader.add_value('com_logo', com_logo if com_logo else 'NULL')
        item_loader.add_xpath('com_md5',"//div[@class='company-box']/p/a/text()")
        com_name=response.xpath("//div[@class='company-box']/p/a/text()").extract_first()
        item_loader.add_value('com_name',com_name)
        item_loader.add_xpath('com_scale',"//div[@class='company-box']/ul/li/span[text()='公司规模：']/following-sibling::*/text()")
        item_loader.add_xpath('com_nature',"//div[@class='company-box']/ul/li/span[text()='公司性质：']/following-sibling::*/text()")
        item_loader.add_xpath('com_industry',"//div[@class='company-box']/ul/li/span[text()='公司行业：']/following-sibling::*/a/text()")
        com_website=response.xpath("//div[@class='company-box']/ul/li/span[text()='公司主页：']/following-sibling::*/a/@href").extract_first()
        item_loader.add_value('com_website',com_website if com_website else 'NULL')
        item_loader.add_xpath('com_address',"//div[@class='company-box']/ul/li/span[text()='公司地址：']/following-sibling::*/text()")
        item_loader.add_value('created_at', time.strftime('%Y-%m-%d %H:%M:%S'))
        
        job_md5=name+com_name+publist_date
        item_loader.add_value('md5',job_md5)
        
        item=item_loader.load_item()
        yield item




