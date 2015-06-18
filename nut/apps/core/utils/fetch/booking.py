# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from hashlib import md5
from django.core.cache import cache
# import re

class Booking():

    def __init__(self, url):
        # self.url = url
        self.html = self.fetch_html(url)
        # print self.html
        self.soup = BeautifulSoup(self.html, from_encoding="UTF-8")
        self.nick = u"booking"

    @property
    def headers(self):
        return self._headers

    @property
    def desc(self):
        return self.soup.title.string[0:-19]

    @property
    def price(self):
        # ptag = self.soup.find("span", id="js_currentPrice")
        # return float(self.price_json['p'])
        rooms = self.soup.select(".lowest-price strong")
        # for room in rooms[:1]:
        #     print room.string

        if len(rooms) > 0:
            room = rooms[0]
            # print i(room.string
            # room_price = re.match(r"(\d+)", room.string)
            room_price = room.string.replace(u'起价：', '').replace(u'元', '')
            return float(room_price)
        # print rooms
        # log.info(ptag)
        # if len(ptag) > 0:
            # return ptag[0].string
        return 0

    @property
    def images(self):
        _images = list()
        optimgs = self.soup.select(".hotel_thumbs_sprite")
        # print optimgs
        for op in optimgs[0:6]:
            optimg = op.attrs.get('data-resized')
            _images.append( optimg )
        #     optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
        #     _images.append("%s.jpg" % optimg)
        # print "OKOKOKO"
        return _images

    @property
    def cid(self):
        return 0

    @property
    def shop_link(self):
        return "http://www.booking.com/"

    @property
    def brand(self):
        return ""

    def fetch_html(self, url):
        key = md5(url).hexdigest()

        res = cache.get(key)
        if res:
            # log.info(res)
            self._headers = res['header']
            return res['body']

        try:
            f = requests.get(url)
        except Exception, e:
            # log.error(e.message)
            raise

        # f = requests.get(url)
        self._headers = f.headers

        res = f.content
        cache.set(key, {'body':res, 'header':self._headers})
        return res



if __name__=="__main__":

    b = Booking("http://www.booking.com/hotel/lk/jetwing-yala.zh-cn.html?sid=f271448c6b6abfb4f7124664d3c56cff")
    # r = b.fetch_html()
    # print r
    # print b.content
    print b.price
    print b.desc

__author__ = 'edison'