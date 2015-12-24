# -*- coding: utf-8 -*-

from apps.core.fetch.fetcher import Fetcher


class Booking(Fetcher):

    # @property
    # def url(self):
    #     url = "http://%s%s" % (self.urlobj.hostname, self.urlobj.path)
    #     return url.rstrip()

    # @property
    # def headers(self):
    #     return self._headers

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
            # print i(room.string
            # room_price = re.match(r"(\d+)", room.string)
            room_price = room.string.replace(u'起价：', '').replace(u'元', '')
            return float(room_price)
        return 0

    @property
    def images(self):
        _images = list()
        optimgs = self.soup.select(".hotel_thumbs_sprite")
        # print optimgs
        for op in optimgs[0:6]:
            optimg = op.attrs.get('data-resized')
            _images.append( optimg )
        return _images

    @property
    def cid(self):
        return 0

    @property
    def shop_link(self):
        return self.hostname
    #     return self.urlobj.hostname

    @property
    def brand(self):
        return ""


if __name__=="__main__":

    b = Booking("http://www.booking.com/hotel/lk/jetwing-yala.zh-cn.html?sid=f271448c6b6abfb4f7124664d3c56cff")
    print b.url
    # r = b.fetch_html()
    # print r
    # print b.content
    print b.origin_id, b.price, b.shop_link, b.desc
    # print b.desc

__author__ = 'edison'