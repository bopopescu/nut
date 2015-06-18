# -*- coding: utf-8 -*-

from apps.core.utils.fetch.spider import Spider
from bs4 import BeautifulSoup
import json


class Amazon(Spider):

    def __init__(self, url):
        # super(Amazon, self).__init__(url)
        self.html = self.fetch_html(url)
        self.soup = BeautifulSoup(self.html, from_encoding="UTF-8")

        self._desc, self._nick, self._category = self.soup.title.string.split(':')

    @property
    def headers(self):
        return self._headers

    @property
    def desc(self):
        return self._desc

    @property
    def nick(self):
        return self._nick

    @property
    def category(self):
        return self._category

    @property
    def price(self):
        return self.soup.select("#price")

    @property
    def images(self):
        images = list()
        optimages = self.soup.select("#altImages ul .a-list-item span img")
        # return opt
        for row in optimages:
            img_link = row.attrs.get('src')
            if len(img_link) == 0:
                continue
            array = img_link.split('_')
            res =  "%s%s" % (array[0], array[-1])
            images.append(res.replace('..', '.'))
        return images

    @property
    def brand(self):
        return ""


if __name__=="__main__":

    a = Amazon("http://www.amazon.cn/Apple-iPhone-6-Plus-4G%E6%99%BA%E8%83%BD%E6%89%8B%E6%9C%BA/dp/B00OB5TGRI/")
    # r = b.fetch_html()
    # print r
    # print b.content
    print a.desc, a.nick, a.category
    print a.price
    # print b.desc


