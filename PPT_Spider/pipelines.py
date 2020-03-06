# -*- coding: utf-8 -*-

import os

import scrapy
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline

from .settings import FILES_STORE


class PptSpiderPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        print(item['ppt_title'])
        yield scrapy.Request(url=item['ppt_url'], meta={'ppt': item})

    def check_file_path(self, ppt_item):
        if not FILES_STORE.endswith('/'):
            file_path = '{}/{}'.format(FILES_STORE, ppt_item['group_name'])
        else:
            file_path = FILES_STORE + ppt_item['group_name']

        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def get_ppt_name(self, ppt_item):
        file_type = ppt_item['ppt_url'].split('.')[-1]
        return '{}.{}'.format(ppt_item['ppt_title'], file_type)

    def file_path(self, request, response=None, info=None):
        ppt_item = request.meta['ppt']
        self.check_file_path(ppt_item)
        ppt_name = self.get_ppt_name(ppt_item)
        return '{}/{}'.format(ppt_item['group_name'], ppt_name)
