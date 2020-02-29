# -*- coding: utf-8 -*-
import scrapy


class A1pptSpider(scrapy.Spider):
    name = '1ppt'
    allowed_domains = ['www.1ppt.com']
    start_urls = ['http://www.1ppt.com/']

    def parse(self, response):
        pass
