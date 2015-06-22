# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json


class OriginIdPipeline(object):

    def process_item(self, item, spider):
        # print "KOKOKOKOKO",item
        # if item.has_key('origin_id'):
        if len(item['origin_id']) > 0:

            return item
        else:
            raise DropItem(item)

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['origin_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['origin_id'])
            return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'ab')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item