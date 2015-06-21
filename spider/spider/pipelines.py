# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class OriginIdPipeline(object):

    def process_item(self, item, spider):
        # print "KOKOKOKOKO",item
        # if item.has_key('origin_id'):
        if len(item['origin_id']) > 0:

            return item
        else:
            raise DropItem(item)