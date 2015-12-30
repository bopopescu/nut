# -*- coding: utf-8 -*-

import re
import json
import urllib2

from hashlib import md5
from django.core.cache import cache
from django.utils.log import getLogger

from apps.fetch.base import BaseFetcher


log = getLogger('django')


class JD(BaseFetcher):

    def __init__(self, entity_url):

        BaseFetcher.__init__(self, entity_url)
        self.high_resolution_pattern = re.compile('hiRes"[\s]*:[\s]*"([^";]+)')
        self.large_resolution_pattern = re.compile('large"[\s]*:[\s]*"([^";]+)')
        self.price_pattern = re.compile(u'(?:￥|\$)\s?(?P<price>\d+\.\d+)')
        self.foreign_price = 0.0
        self.entity_url = entity_url
        self.origin_id = self.get_origin_id()
        self.expected_element = 'span.tm-price'
        self.shop_link = self.get_shop_link()
        self.shop_nick = self.get_nick()

    def get_origin_id(self):
        ids = re.findall(r'\d+', self.entity_url)
        if len(ids) > 0:
            return ids[0]

    def fetch_html(self):
        url = 'http://item.jd.com/%s.html' % self.origin_id
        key = md5(url).hexdigest()
        res = cache.get(key)
        if res:
            return res
        try:
            f = urllib2.urlopen(url)
        except Exception, e:
            log.error("ERROR: %s" % e.message)
            raise

        self._headers = f.headers
        res = f.read()
        cache.set(key, res)
        return res

    def fetch_price(self):
        price_link = "http://p.3.cn/prices/get?skuid=J_%s&type=1&area=1_72_4137&callback=cnp" % self.origin_id
        resp = urllib2.urlopen(price_link)
        data = resp.read()
        data = data[5:-4]
        return json.loads(data)

    @property
    def title(self):
        self._title = self.soup.title.string
        return self._title

    @property
    def brand(self):
        brandtag = self.soup.select("ul.detail-list li a")
        self._brand = ""
        if len(brandtag)>0:
            self._brand = brandtag[0].string
            self._brand = self._brand.replace(u"旗舰店","")
            self._brand = self._brand.replace(u"官方","")
        return self._brand

    @property
    def cid(self):
        cattag = self.soup.select("html body div.w div.breadcrumb span a")[1]
        catlink = cattag.attrs['href']
        catstr = re.findall(r'\d+',catlink)
        category = [int(x) for x in catstr]
        # print category
        return category[-1]

    def get_shop_link(self):
        tmp = re.findall(r'店铺.*>(.+)</a>', self.html)
        # _shop_link = ""
        if len(tmp)>0:
            self.nick = tmp[0]
            link = re.findall(r'店铺.* href="(.+)">', self.html)[0]
            _shop_link = link[:-16]
        else:
            self.nick="京东"
            _shop_link = "http://jd.com"

        return _shop_link

    @property
    def imgs(self):
        imgtags = self.soup.select("html body div.w div#product-intro \
                div#preview div#spec-list div.spec-items ul li img")
        imgs = []

        for tag in imgtags:
            src = tag['src']
            src = src.replace('com/n5','com/n1')
            imgs.append(src)
        return imgs

    @property
    def price(self):

        return float(self.price_json['p'])


if __name__ == '__main__':

    result = JD(210347)

    print result.title
