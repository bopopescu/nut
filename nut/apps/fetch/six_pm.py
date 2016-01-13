# -*- coding: utf-8 -*-

from hashlib import md5
from apps.fetch.base import BaseFetcher


class SixPM(BaseFetcher):

    def __init__(self, entity_url):
        BaseFetcher.__init__(self, entity_url)
        self.entity_url = entity_url

    @property
    def origin_id(self):
        key = md5(self.entity_url).hexdigest()
        return key

    @property
    def link(self):
        return self.entity_url

    @property
    def nick(self):
        return '6pm'

    @property
    def brand(self):
        brand = self.soup.select("#productStage h1 .brand")
        return brand[0].string

    @property
    def desc(self):
        desc = self.soup.select("#productStage h1 .link")
        return desc[0].string

    @property
    def cid(self):
        return 0

    @property
    def shop_link(self):
        return self.origin_source

    @property
    def price(self):
        pricetag = self.soup.select("#priceSlot .price")
        price = pricetag[0].string.replace('$', '')
        return round(float(price) * 6.2, 2)

    @property
    def get_images(self):
        images = list()
        optimages = self.soup.select("#productImages ul li a span img")
        if len(optimages) > 0:
            for row in optimages:
                image = row.attrs.get('src')
                image = image.replace('_THUMBNAILS', '')
                # print image
                images.append(image)
        return images
        # print optimages


if __name__=="__main__":

    pm = SixPM("http://www.6pm.com/michael-antonio-avalon-brown")
    print pm.price
    print pm.brand
    print pm.url
    print pm.images
    print pm.desc

__author__ = 'edison'
