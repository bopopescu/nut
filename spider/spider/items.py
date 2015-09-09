# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    origin_id = scrapy.Field()
    origin_source = scrapy.Field()
    brand = scrapy.Field()
    title = scrapy.Field()
    cid = scrapy.Field()
    image_urls = scrapy.Field()
    foreign_price = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    shop_link = scrapy.Field()
    seller = scrapy.Field()
    link = scrapy.Field()
    update_selection_status = scrapy.Field()