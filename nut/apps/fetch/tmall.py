# -*- coding: utf-8 -*-

import re

from urllib import unquote
from django.utils.log import getLogger

from apps.fetch.common import clean_price_string
from apps.fetch.fetcher import Fetcher


log = getLogger('django')
IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"


class Tmall(Fetcher):
    def __init__(self, entity_url):
        Fetcher.__init__(self, entity_url)
        self.high_resolution_pattern = re.compile('hiRes"[\s]*:[\s]*"([^";]+)')
        self.large_resolution_pattern = re.compile('large"[\s]*:[\s]*"([^";]+)')
        self.price_pattern = re.compile(u'(?:￥|\$)\s?(?P<price>\d+\.\d+)')
        self.foreign_price = 0.0
        self.entity_url = entity_url
        self.origin_id = self.get_origin_id()
        self.expected_element = 'span.tm-price'
        self.shop_link = self.hostname

    @property
    def nick(self):
        self._nick = self._headers.get('at_nick')
        if not self._nick:
            return ""
        return unquote(self._nick)

    @property
    def link(self):
        link = 'http://detail.tmall.com/item.htm?id=%s' % self.origin_id
        return link

    def get_origin_id(self):
        params = self.entity_url.split("?")[1]
        for param in params.split("&"):
            tokens = param.split("=")
            if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
                return tokens[1]

    @property
    def cid(self):
        cat = self.headers.get('X-Category')
        try:
            _cid = cat.split('/')
            return _cid[-1]
        except AttributeError, e:
            log.error("Error: %s", e.message)
        return 0

    @property
    def desc(self):
        return self.soup.title.string[0:-12]

    @property
    def price(self):
        price_tag = self.get_price_tag()
        if not price_tag:
            return 0.0
        return price_tag

    def get_price_tag(self):
        price_tag_names = (
            'span.tm-price',
        )
        for price_tag_name in price_tag_names:
            price_tags = self.soup.select(price_tag_name)
            if len(price_tags) > 0:
                prices = []
                for price_tag in price_tags:
                    if price_tag.text:
                        prices.append(clean_price_string(price_tag.text))
                prices.sort()
                return prices[0]

    @property
    def brand(self):
        seller_soup = self.soup.select("ul.attributes-list li")
        if not seller_soup:
            seller_soup = self.soup.select("ul#J_AttrUL li")
        if seller_soup > 0:
            for brand_li in seller_soup:
                if brand_li.text.find(u'品牌') >= 0:
                    return brand_li.text.split(u':')[1].strip()
        return ''

    @property
    def images(self):
        _images = list()
        fimg = self.soup.select("#J_ImgBooth")

        fjpg = fimg[0].attrs.get('data-src')
        if not fjpg:
            fjpg = fimg[0].attrs.get('src')

        fjpg = re.sub(IMG_POSTFIX, "", fjpg)

        if "http" not in fjpg:
            fjpg = "http:" + fjpg

        _images.append(fjpg)

        optimgs = self.soup.select("ul#J_UlThumb li a img")

        for op in optimgs:
            try:
                optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
            except TypeError, e:
                optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('data-src'))
            if optimg in _images:
                continue
            _images.append(optimg)
        return _images

    @property
    def shoplink(self):
        shopidtag = re.findall('shopId:"(\d+)', self.html)

        if len(shopidtag) > 0:
            shoplink = "http://shop"+shopidtag[0]+".taobao.com"
            return shoplink
        return "http://chaoshi.tmall.com/"
