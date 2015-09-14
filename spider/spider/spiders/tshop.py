# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from spider.items import GItem

IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"

class TaobaoShop(CrawlSpider):
    name = "tshop"
    allowed_domains = ["item.taobao.com"]
    # start_urls = [
    #         "http://shop33559902.taobao.com/"
    #         # "http://www.guoku.com/selected/"
    #     ]
    #
    rules = (
        Rule(LinkExtractor(allow=('item\.htm', )), callback='parse_item'),
    )

    def __init__(self, shop_id, update_selection_status=False, *args, **kwargs):
        super(TaobaoShop, self).__init__(*args, **kwargs)
        self.update_selection_status = update_selection_status
        self.shop_id = shop_id
        self.start_urls = [
            "http://shop%s.taobao.com/" % self.shop_id
            # "http://www.guoku.com/selected/"
        ]

    # def parse(self, response):
    #     self.logger.info(response.url)

    def parse_item(self, response):
        item['update_selection_status'] = self.update_selection_status
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = GItem()
        item['status'] = 2
        try:
            item['origin_id'] = response.headers['At_Itemid']
        except KeyError:
            item['origin_id'] = self.item_id


        item['link'] = response.url
        if 'noitem.htm' in response.url:
            item['status'] = 0
            return item

        metas = response.xpath('//meta/@content').extract()
        # self.log(shop)
        shopId = 0
        seller = 0
        for row in metas:
            m = re.search(r'shopId=\d+', row)
            if m:
                shopId = re.sub('shopId=', '', m.group())
            s = re.search(r'userid=\d+', row)
            if s:
                seller = re.sub('userid=', '', s.group())

        if seller != 0:
            item['seller'] = seller

        item['shop_link'] =  "http://shop%s.taobao.com/" % self.shop_id

        cat_id = 0
        try:
            cat = response.headers['At_Cat']
            cat_id = cat.split('_')[-1]
        except KeyError:
            pass

        soldout = response.xpath('//p[@class="tb-hint"]/strong/text()').extract()
        item['price'] = self.get_price(response)
        item['cid'] = cat_id
        item['image_urls'] = self.get_images(response)

        if len(soldout) > 0:
            item['status'] = 1

        return item

    def get_images(self, response):
        images = list()
        origin_images = response.xpath('//img[@id="J_ImgBooth"]/@data-src').extract()
        optimgs = response.xpath('//ul[@id="J_UlThumb"]/li/div/a/img/@data-src').extract()
        # self.log(optimgs)
        if len(optimgs) > 1:
            origin_images += optimgs[1:]
        for img in origin_images:
            if 'http' not in img:
                img = 'http:' + img
            img = re.sub(IMG_POSTFIX, "", img)
            images.append(img)

        return images

    def get_price(self, response):
        price = response.xpath('//strong[@id="J_StrPrice"]/em[@class="tb-rmb-num"]/text()').extract()
        if len(price) == 0:
            return 0
            # price = response.xpath('//dl[@id="J_StrPriceModBox"]/dd').extract()
        # self.log(price)

        price = price[0].split('-')
        # self.log(price)
        if len(price) == 1:
            return float(price[0])
        else:
            return float(price[1])


__author__ = 'edison'
