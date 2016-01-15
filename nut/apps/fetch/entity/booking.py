# -*- coding: utf-8 -*-
from urlparse import urlparse

from apps.fetch.entity.base import BaseFetcher


class Booking(BaseFetcher):

    def __init__(self, entity_url):
        BaseFetcher.__init__(self, entity_url)
        self.entity_url = entity_url
        self.origin_id = self.get_origin_id()
        self._headers = None

    @property
    def link(self):
        url_obj = urlparse(self.entity_url)
        url = "http://%s%s" % (url_obj.hostname, url_obj.path)
        return url.rstrip()

    @property
    def headers(self):
        return self._headers

    def get_origin_id(self):
        params = self.entity_url.split("?")[1]
        for param in params.split(";"):
            tokens = param.split("=")
            if len(tokens) >= 2 and tokens[0] == "sid":
                return tokens[1]

    @property
    def nick(self):
        return "booking"

    @property
    def desc(self):
        return self.soup.title.string[0:-19]

    @property
    def price(self):
        rooms = self.soup.select(".lowest-price strong")

        if len(rooms) > 0:
            room = rooms[0]
            room_price = room.string.replace(u'起价：', '').replace(u'元', '')
            return float(room_price)
        return 0

    @property
    def images(self):
        _images = list()
        optimgs = self.soup.select(".hotel_thumbs_sprite")
        for op in optimgs[0:6]:
            optimg = op.attrs.get('data-resized')
            _images.append( optimg )
        return _images

    @property
    def cid(self):
        return 0

    @property
    def shop_link(self):
        return self.origin_source

    @property
    def brand(self):
        return ""
