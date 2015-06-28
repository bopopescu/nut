# -*- coding: utf-8 -*-
import scrapy
import re
from spider.items import GItem

IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"


class TaobaoSpider(scrapy.Spider):
    name = "taobao"
    allowed_domains = ["taobao.com"]

    def __init__(self, item_id, *args, **kwargs):
        super(TaobaoSpider, self).__init__(*args, **kwargs)
        self.item_id = item_id
        self.start_urls = [
            "http://item.taobao.com/item.html?id=%s" % self.item_id
        ]

    def parse(self, response):
        # self.log(response.headers)
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

        if shopId != 0:
            item['shop_link'] = "http://shop%s.taobao.com" % shopId
                # shopId = m.group()
        #     print re.findall('shopId:"(\d+)', row)
            # self.log(row)
        # self.log(shopId)
        # price = self.get_price(response)

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

        cat_id = 0
        try:
            cat = response.headers['At_Cat']
            cat_id = cat.split('_')[-1]
        except KeyError:
            pass

        soldout = response.xpath('//p[@class="tb-hint"]/strong/text()').extract()
        item['price'] = self.get_price(response)
        item['cid'] = cat_id
        item['image_urls'] = images

        if len(soldout) > 0:
            item['status'] = 1
        # item['link'] = response.url

        self.log(item)
        return item

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