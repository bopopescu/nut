# -*- coding: utf-8 -*-

import re
from urlparse import urlparse

from django.utils.log import getLogger

from apps.fetch.entity.base import BaseFetcher


log = getLogger('django')
IMG_POSTFIX = "_\d+_\d+.*\.jpg|_b\.jpg"


class Kaola(BaseFetcher):
    def __init__(self, entity_url):
        BaseFetcher.__init__(self, entity_url)
        self.entity_url = entity_url
        self.origin_id = self.get_origin_id()

    def get_origin_id(self):
        ids = re.findall(r'\d+', self.entity_url)
        if len(ids) > 0:
            return ids[0]

    @property
    def shop_nick(self):
        return u"考拉海购"

    @property
    def desc(self):
        return self.soup.title.string[0:-5]

    @property
    def link(self):
        url_obj = urlparse(self.entity_url)
        return "http://%s%s" % (url_obj.hostname, url_obj.path)

    @property
    def images(self):
        _images = list()
        optimgs = self.soup.select("#litimgUl li a img")

        for op in optimgs:
            optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
            _images.append("%s.jpg" % optimg)

        return _images

    @property
    def price(self):
        ptag = self.soup.select("#js_currentPrice > span")
        log.info(ptag)
        if len(ptag) > 0:
            return ptag[0].string
        return 0

    @property
    def cid(self):
        return 0

    @property
    def brand(self):
        _brand = self.soup.select("#goodsDetail > ul > li")
        if len(_brand) > 0:
            return _brand[0].string.replace(u'商品品牌：', '')
        return ''

    @property
    def shop_link(self):
        return "http://www.kaola.com/"
