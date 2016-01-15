# -*- coding: utf-8 -*-

import json
import re
import urllib2

from apps.fetch.entity.base import BaseFetcher
from django.utils.log import getLogger

from apps.fetch.common import clean_price_string


log = getLogger('django')


class JD(BaseFetcher):
    def __init__(self, entity_url, use_phantom=True):
        BaseFetcher.__init__(self, entity_url)
        self.entity_url = entity_url
        self.use_phantom = use_phantom
        self.expected_element = 'span.tm-price'
        self.foreign_price = 0.0
        self.origin_id = self.get_origin_id()
        self.brand_pattern = re.compile(u'品牌： (?P<brand>\w+&\w)',
                                        re.UNICODE | re.MULTILINE)

        self._link = ''

    def get_origin_id(self):
        ids = re.findall(r'\d+', self.entity_url)
        if len(ids) > 0:
            return ids[0]

    @property
    def link(self):
        if not self._link:
            self._link = 'http://item.jd.com/%s.html' % self.origin_id
        return self._link

    @property
    def title(self):
        title = self.soup.title.string
        return title

    @property
    def brand(self):
        brand_tag = self.soup.select("ul.detail-list li a")
        self._brand = ""
        brand_string = ''
        if len(brand_tag) > 0:
            brand_string = brand_tag[0].string

        if not brand_string:
            brand_tag = self.soup.select('div.brand-logo img')
            if brand_tag:
                brand_string = brand_tag[0].attrs.get('title')

        brand_string = brand_string.replace(u"京东旗舰店", "")
        brand_string = brand_string.replace(u"旗舰店", "")
        brand_string = brand_string.replace(u"官方", "")
        self._brand = brand_string
        return self._brand

    @property
    def cid(self):
        cattag = self.soup.select("html body div.w div.breadcrumb span a")[1]
        catlink = cattag.attrs['href']
        catstr = re.findall(r'\d+', catlink)
        category = [int(x) for x in catstr]
        return category[-1]

    @property
    def shop_link(self):
        _shop_link_tag = re.findall(r'店铺.*>(.+)</a>', self.html_source)
        _shop_link = "http://jd.com"
        if len(_shop_link_tag) > 0:
            self._shop_nick = _shop_link_tag[0]
            link = re.findall(r'店铺.* href="(.+)">', self.html_source)[0]
            _shop_link = link[:-16]

        if not _shop_link_tag:
            _shop_link_tag = self.soup.select('div.brand-logo a')
            if _shop_link_tag:
                _shop_link = _shop_link_tag[0].attrs.get('href')

        if not _shop_link_tag:
            _shop_link_tag = self.soup.select('a.name')
            if _shop_link_tag:
                _shop_link = _shop_link_tag[0].attrs.get('href')

        if not _shop_link_tag:
            _shop_link_tag = self.soup.select('a.J-enter-shop')
            if _shop_link_tag:
                _shop_link = _shop_link_tag[0].attrs.get('href')

        return _shop_link

    @property
    def shop_nick(self):
        if self._shop_nick:
            return self._shop_nick
        _shop_name_tags = self.soup.select('div.brand-logo img')
        if _shop_name_tags:
            return _shop_name_tags[0].attrs.get('title')

        _shop_name_tags = self.soup.select('a.name')
        if _shop_name_tags:
            shop_name = _shop_name_tags[0].attrs.get('title')
            if not shop_name:
                shop_name = _shop_name_tags[0].text
            return shop_name
        return u'京东'

    @property
    def images(self):
        img_tags = self.soup.select("html body div.w div#product-intro \
                div#preview div#spec-list div.spec-items ul li img")
        img_list = []

        for tag in img_tags:
            src = tag['src']
            src = src.replace('com/n5', 'com/n1')
            if not src.startswith('http') and not src.startswith('https'):
                src = 'http:'+src
            img_list.append(src)

        img_list = list(set(img_list))
        self._images = img_list
        if img_list:
            self._chief_image = img_list[0]
        return img_list

    @property
    def price(self):
        price = '0.0'
        price_tag = self.soup.select('strong#jd-price')
        if price_tag:
            price = price_tag[0].text

        if not price:
            price = self.price_json['p']

        price = clean_price_string(price)
        return float(price)

    @property
    def price_json(self):
        price_link = "http://p.3.cn/prices/get?skuid=J_%s&type=1&area=1_72_4137&callback=cnp" % self.origin_id
        resp = urllib2.urlopen(price_link)
        data = resp.read()
        data = data[5:-4]
        return json.loads(data)


if __name__ == '__main__':
    result = JD(210347)

    print result.title
