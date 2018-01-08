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


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allow_domains = ['jobs.zhaopin.com']
    base_url = 'http://jobs.zhaopin.com'
    # start_urls = ['http://jobs.zhaopin.com/']

    custom_settings = {
        'JOBDIR':'/Users/yexianyong/Desktop/spider/job_dir/zhilian'
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
        print('爬虫已关闭',self.current_city_index,self.current_page)

    def spider_open(self):
        print('爬虫已开始',self.current_city_index,self.current_page,self.state)


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
        # print(response)

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        pass





