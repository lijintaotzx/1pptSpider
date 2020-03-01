# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PPTSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    group_name = scrapy.Field()
    group_url = scrapy.Field()

    ppt_title = scrapy.Field()
    ppt_url = scrapy.Field()
