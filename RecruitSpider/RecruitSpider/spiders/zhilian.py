#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue on 2017/12/29


import scrapy
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from RecruitSpider.tools import tool
from urllib import parse as urllib_parse


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allow_domains = ['jobs.zhaopin.com']
    base_url = 'http://jobs.zhaopin.com'
    # start_urls = ['http://jobs.zhaopin.com/']

    custom_settings = {

    }
    cities = tool.get_city_pinyin()
    current_city_index = 0
    current_page = 1

    def start_requests(self):
        start_url = urllib_parse.urljoin(self.base_url,
                                         self.cities[self.current_city_index] + ('/p{}/'.format(self.current_page)))
        print(len(self.cities))
        yield Request(url=start_url, callback=self.parse)

    def parse(self, response):
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
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        print(response)








