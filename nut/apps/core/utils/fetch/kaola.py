# -*- coding: utf-8 -*-

# import requests
# from hashlib import md5
# from bs4 import BeautifulSoup
# from django.core.cache import cache
from django.utils.log import getLogger
import re

from apps.core.utils.fetch.spider import Spider

log = getLogger('django')

IMG_POSTFIX = "_\d+_\d+.*\.jpg|_b\.jpg"

class Kaola(Spider):

    @property
    def origin_id(self):
        p = re.compile('\d+')
        m = p.search(self.urlobj.path)
        return m.group()

    @property
    def nick(self):
        return u"考拉海购"

    @property
    def desc(self):
        return self.soup.title.string[0:-5]

    @property
    def buy_link(self):
        return "http://%s%s" % (self.urlobj.hostname, self.urlobj.path)

    @property
    def images(self):
        _images = list()
        optimgs = self.soup.select("#litimgUl li a img")

        for op in optimgs:
            # optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
            optimg = re.sub(r'\?image.*', "", op.attrs.get('src'))
            # optimg = op.attrs.get('src')
            _images.append(optimg)

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

    # def fetch_html(self):
    #     url = 'http://www.kaola.com/product/%s.html' % self.kaola_id
    #     key = md5(url).hexdigest()
    #
    #     res = cache.get(key)
    #     if res:
    #         # log.info(res)
    #         self._headers = res['header']
    #         return res['body']
    #
    #     try:
    #         f = requests.get(url)
    #     except Exception, e:
    #         log.error(e.message)
    #         raise
    #
    #     self._headers = f.headers
    #     res = f.text
    #     cache.set(key, {'body':res, 'header':self._headers})
    #     return res
        # res = f.read()
        # cache.set(key, {'body':res, 'header':self._headers})
        # return res

if __name__=="__main__":
    k = Kaola('http://www.kaola.com/product/8505.html?from=RECOMMEND')
    # print k.origin_id, k.nick, k.hostname, k.shop_link, k.buy_link
    print k.html

__author__ = 'edison'
