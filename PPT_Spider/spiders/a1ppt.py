# -*- coding: utf-8 -*-
import scrapy

from ..items import PPTSpiderItem


class A1pptSpider(scrapy.Spider):
    name = '1ppt'
    allowed_domains = ['www.1ppt.com']
    start_urls = ['http://www.1ppt.com/xiazai/']

    ppt_url = 'http://www.1ppt.com'

    def parse(self, response):
        '''
        解析主页面PPT分组
        :param response:
        :return:
        '''
        group_list = response.xpath('//div[@class="col_nav clearfix"]/ul/li')[1:]

        for group in group_list:
            item = PPTSpiderItem()
            item['group_name'] = group.xpath('./a/text()').get()
            item['group_url'] = self.ppt_url + group.xpath('./a/@href').get()

            yield scrapy.Request(url=item['group_url'], meta={'group': item}, callback=self.parse_all_group_url)

    def parse_all_group_url(self, response):
        """
        yield 所有分组内PPT，所有分页url
        :param response:
        :return:
        """
        group = response.meta['group']
        index_url = group['group_url']

        group_url_list = [index_url]
        for group_page in response.xpath('//ul[@class="pages"]/li')[2:]:
            url = index_url + group_page.xpath('./a/@href').get()
            group_url_list.append(url)

        for url in group_url_list:
            yield scrapy.Request(url=url, meta={'group': group}, callback=self.parse_ppt_page)

    def parse_ppt_page(self, response):
        """
        解析分组内PPT详情页
        :param response:
        :return:
        """
        group = response.meta['group']

        ppt_page_list = response.xpath('//ul[@class="tplist"]/li')
        for ppt_page in ppt_page_list:
            ppt_page_url = self.ppt_url + ppt_page.xpath('./a/@href').get()
            yield scrapy.Request(url=ppt_page_url, meta={'group': group}, callback=self.parse_ppt)

    def parse_ppt(self, response):
        """
        解析PPT标题及下载链接
        :param response:
        :return:
        """
        group = response.meta['group']

        ppt_title = response.xpath('//div[@class="ppt_info clearfix"]/h1/text()').get()
        ppt_url = response.xpath('//ul[@class="downurllist"]/li/a/@href').get()
        item = PPTSpiderItem()
        item['group_name'] = group['group_name']
        item['group_url'] = group['group_url']
        item['ppt_title'] = ppt_title
        item['ppt_url'] = ppt_url

        yield item
