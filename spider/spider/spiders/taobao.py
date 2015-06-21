# -*- coding: utf-8 -*-
import scrapy
from spider.items import GItem


IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"


class TaobaoSpider(scrapy.Spider):
    name = "taobao"
    allowed_domains = ["taobao.com"]

    def __init__(self, item_id, *args, **kwargs):
        super(TaobaoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "http://item.taobao.com/item.html?id=%s" % item_id
        ]

    def parse(self, response):
        self.log(response.headers)

        price = response.xpath('//strong[@id="J_StrPrice"]/em[@class="tb-rmb-num"]/text()').extract()

        cat = response.headers['At_Cat']
        cat_id = cat.split('_')[-1]

        item = GItem()
        item['origin_id'] = response.headers['At_Itemid']
        item['price'] = price
        item['cid'] = cat_id

        return item
