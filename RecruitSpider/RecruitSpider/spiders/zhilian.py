#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue on 2017/12/29
from scrapy.http import Request,Response
from scrapy import signals
from scrapy.conf import settings
from urllib.parse import urlparse
from urllib import parse as urllib_parse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from RecruitSpider.items import *
import time,os
from RecruitSpider.tools import tool


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allow_domains = ['jobs.zhaopin.com']
    base_url = 'http://jobs.zhaopin.com'
    
    cities = tool.get_city_pinyin()
    #从数据库中读取现有的job_url,然后在发起job detail页面的请求时进行一个判断是否已经请求过。
    #scrapy启动之后已经爬取的链接通过scrapy自身去重
    requested_job_url_md5=tool.get_job_url_md5()

    headers = {
        'Host'                     : 'jobs.zhaopin.com',
        'Connection'               : 'keep-alive',
        'Cache-Control'            : 'max-age=0',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent'               : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding'          : 'gzip, deflate',
        'Accept-Language'          : 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie'                   : '__utma=269921210.890444320.1515986456.1515986456.1515986456.1; __utmc=269921210; __utmz=269921210.1515986456.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; dywea=95841923.3320700297463268000.1515986456.1515986456.1515986456.1; dywec=95841923; dywez=95841923.1515986456.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; _jzqa=1.2610123500841465300.1515986456.1515986456.1515986456.1; _jzqc=1; _jzqckmp=1; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; firstchannelurl=https%3A//passport.zhaopin.com/account/login%3FBkUrl%3Dhttp%253a%252f%252fi.zhaopin.com%252f; pcc=r=677854105&t=0; lastchannelurl=https%3A//passport.zhaopin.com/account/login%3FBkUrl%3Dhttp%253a%252f%252fi.zhaopin.com%252f; dywem=95841923.y; userphoto=; userwork=5; bindmob=0; rinfo=JM037508819R90500000000_1; monitorlogin=Y; NTKF_T2D_CLIENTID=guestAEBBD54F-792E-7A12-3F5C-F7D5B92EBB48; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_603750881,tid:1515986467118692}; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1515985115; usermob=5E6F466B566952685377446F59735F6451665C6A41769; JSweixinNum=2; LastCity=%e6%88%90%e9%83%bd; LastCity%5Fid=801; loginreleased=1; dyweb=95841923.7.10.1515986456; __utmb=269921210.7.10.1515986456; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1515986741; bdshare_firstime=1515986741523; _qzja=1.1506218625.1515986741632.1515986741632.1515986741632.1515986741632.1515986741632.0.0.0.1.1; _qzjc=1; _qzjto=1.1.0; _jzqb=1.4.10.1515986456.1; _qzjb=1.1515986741632.1.0.0.0; stayTimeCookie=1515986742138; referrerUrl=http%3A//jobs.zhaopin.com/'
    }
    
    requested_url_list_file=open(os.path.join(settings.get('JOBDIR'),'requested_url.txt'),'a')
    
    
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ZhilianSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_open, signals.spider_opened)
        crawler.signals.connect(spider.spider_close, signals.spider_closed)
        return spider

    def spider_close(self):
        self.requested_url_list_file.close()
        print('爬虫已关闭')

    def spider_open(self):
        print('爬虫已开始')


    def start_requests(self):
        for city in self.cities[24:]:
            self.requested_url_list_file.write('{}\n'.format(city))
            print(city)
            for index in range(100):
                temp_url = urllib_parse.urljoin(self.base_url,
                        city + ('/p{}/'.format(index+1)))
                yield Request(url=temp_url, callback=self.parse, headers=self.headers, errback=self.handle_error)

        

    def parse(self, response):
        self.requested_url_list_file.write('{}\n'.format(response))
        print(response)
        # raise CloseSpider(reason='智联爬取完毕...')
        #解析list
        job_list = response.xpath("//ul[contains(@class,'search_list')]/li/div[contains(@class,'details_container')]")
        for job_node in job_list:
            job_url = job_node.xpath("span[@class='post']/a/@href").extract_first()
            if not tool.get_md5(job_url) in self.requested_job_url_md5:
                yield Request(url=job_url, callback=self.parse_job_detail, headers=self.headers,
                        errback=self.handle_error, priority=1)
            
    
    def handle_error(self,failure):
        # log all failures
        self.logger.error(repr(failure))
    
        # in case you want to do something special for some errors,
        # you may need the failure's type:
    
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
    
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
    
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            

    def parse_job_detail(self,response):
        print(response.url)
        # zhilian_job
        item_loader=BaseItemLoader(item=RecruitspiderItem(),response=response)
        item_loader.add_xpath('name',"//div[@class='top-fixed-box']/div/div/h1/text()")
        label=response.xpath("//div[@class='top-fixed-box']//div[@class='welfare-tab-box']/span/text()").extract()
        item_loader.add_value('label',','.join(label) if label else None)
        item_loader.add_xpath('salary_low',"//ul/li/span[text()='职位月薪：']/following-sibling::*/text()")
        item_loader.add_xpath('salary_high',"//ul/li/span[text()='职位月薪：']/following-sibling::*/text()")
        item_loader.add_xpath('city',"//ul/li/span[text()='工作地点：']/following-sibling::*/a/text()")
        item_loader.add_xpath('publish_date',"//ul/li/span[text()='发布日期：']/following-sibling::*/span/text()")
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
        item_loader.add_xpath('com_logo',"//div[@class='company-box']/p[@class='img-border']/a/img/@src")
        item_loader.add_xpath('com_md5',"//div[@class='company-box']/p/a/text()")
        item_loader.add_xpath('com_name',"//div[@class='company-box']/p/a/text()")
        item_loader.add_xpath('com_scale',"//div[@class='company-box']/ul/li/span[text()='公司规模：']/following-sibling::*/text()")
        item_loader.add_xpath('com_nature',"//div[@class='company-box']/ul/li/span[text()='公司性质：']/following-sibling::*/text()")
        item_loader.add_xpath('com_industry',"//div[@class='company-box']/ul/li/span[text()='公司行业：']/following-sibling::*/a/text()")
        item_loader.add_xpath('com_website',"//div[@class='company-box']/ul/li/span[text()='公司主页：']/following-sibling::*/a/@href")
        item_loader.add_xpath('com_address',"//div[@class='company-box']/ul/li/span[text()='公司地址：']/following-sibling::*/text()")
        item_loader.add_value('created_at', time.strftime('%Y-%m-%d %H:%M:%S'))
        
        md5_origin='{}{}{}'.format(item_loader.get_output_value('name'),item_loader.get_output_value('com_name'),item_loader.get_output_value('publish_date'))
        item_loader.add_value('md5',tool.get_md5(md5_origin))
        
        item=item_loader.load_item()
        yield item



    
