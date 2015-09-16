# -*- coding: utf-8 -*-

import scrapy
import re
from spider import utiles
from spider.items import GItem


class AmazonSpider(scrapy.Spider):
    """
    A spider of Amazon.com and Amazon.cn
    """
    name = 'amazon'
    allowed_domains = [
        'http://www.amazon.cn',
        'http://www.amazon.com']

    def __init__(self, item_id, domain, update_selection_status=False,
                 *args, **kwargs):
        """
        Args:
            item_id: Id of a entity.
            domain: amazon.com or amazon.cn
        """
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.item_id = item_id
        self.domain = domain
        self.currency_code = self.get_currency_code()
        self.update_selection_status = update_selection_status
        self.start_urls = [
            'http://%s/gp/product/%s' % (self.domain, self.item_id)
        ]
        self.high_resolution_pattern = re.compile('hiRes"[\s]*:[\s]*"([^";]+)')

    def parse(self, response):
        item = GItem()

        item['update_selection_status'] = self.update_selection_status
        item['origin_id'] = self.item_id
        item['link'] = response.url
        item['status'] = self.get_item_status(response)

        # get brand
        item['seller'] = self.get_seller(response)

        # get category
        cat_id = 0
        cate_list = response.xpath(
            "//div[@id='wayfinding-breadcrumbs_feature_div']"
            "/ul/li/span/a/@href").extract()
        if cate_list:
            cat_id = cate_list[0].split('=')[-1]
        item['cid'] = cat_id

        # get price
        item['price'], item['foreign_price'] = self.get_price(response)

        # get images
        item['image_urls'] = self.get_images(response)

        return item

    def get_item_status(self, response):
        if response.status == 404:  # remove
            return 2
        if len(response.xpath("//div[@id='outOfStock']")
                .extract()) > 0:  # sold out
            return 1
        return 0

    def get_price(self, response):
        price_xpath = response.xpath(
            "//span[@id='priceblock_ourprice']/text()").extract()
        if len(price_xpath) == 0:
            return 0, 0
        else:
            price = price_xpath[0].strip()[1:]
            print self.currency_code, price_xpath[0][:1]
            if self.currency_code == 'USD' and price_xpath[0][:1] == '$':
                price = float(price)
                cny_price = utiles.currency_converting('USD', price)
                return cny_price, price
            return price, None

    def get_seller(self, response):
        brand_xpath_1 = response.xpath("//img[@id='logoByLine']")
        brand_xpath_2 = response.xpath("//a[@id='brand']")
        seller = ''
        if len(brand_xpath_1) > 0:
            seller = brand_xpath_1.xpath(
                "@title").extract() or brand_xpath_1.xpath("@alt").extract()
        if not seller and len(brand_xpath_2) > 0:
            seller = brand_xpath_2[0].xpath("text()").extract()[0]
        return seller

    def get_images(self, response):
        image_js = response.xpath(
            "//div[@id='imageBlock_feature_div']").extract()
        if image_js:
            images = self.high_resolution_pattern.findall(image_js[0])
            return images
        return []

    def get_currency_code(self):
        if self.domain.endswith('amazon.com'):
            return 'USD'
        elif self.domain.endswith('amazon.cn'):
            return 'CNY'
        return ''
