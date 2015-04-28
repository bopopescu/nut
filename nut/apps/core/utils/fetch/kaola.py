# -*- coding: utf-8 -*-

import requests
from hashlib import md5
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.utils.log import getLogger
import re

log = getLogger('django')

IMG_POSTFIX = "_\d+_\d+.*\.jpg|_b\.jpg"

class Kaola():


    def __init__(self, id, *args, **kwargs):
        self.kaola_id = id
        self.html = self.fetch_html()
        self.soup = BeautifulSoup(self.html, from_encoding="UTF-8")
        self.nick="考拉海购"
        # log.info(self.soup)

    @property
    def headers(self):
        return self._headers

    @property
    def desc(self):
        return self.soup.title.string[0:-5]

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
        # ptag = self.soup.find("span", id="js_currentPrice")
        # return float(self.price_json['p'])
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
        # log.info(_brand)
        if len(_brand) > 0:
            return  _brand[0].string.replace(u'商品品牌：', '')
        return ''
        # return _brand

    @property
    def shop_link(self):

        return "http://www.kaola.com/"

    def fetch_html(self):
        url = 'http://www.kaola.com/product/%s.html' % self.kaola_id
        key = md5(url).hexdigest()

        res = cache.get(key)
        if res:
            # log.info(res)
            self._headers = res['header']
            return res['body']

        try:
            f = requests.get(url)
        except Exception, e:
            log.error(e.message)
            raise

        self._headers = f.headers
        res = f.text
        cache.set(key, {'body':res, 'header':self._headers})
        return res
        # res = f.read()
        # cache.set(key, {'body':res, 'header':self._headers})
        # return res

__author__ = 'edison'
