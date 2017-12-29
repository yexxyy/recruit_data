#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue on 2017/12/29


import scrapy


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allow_domains=['jobs.zhaopin.com']
    start_urls=['http://jobs.zhaopin.com/']
    
    
    
    def parse(self, response):
        pass
    