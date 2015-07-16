# -*- coding: utf-8 -*-

from apps.core.utils.fetch.spider import Spider
from urlparse import urljoin
from hashlib import md5
import re


class Amazon(Spider):

    def __init__(self, url):
        super(Amazon, self).__init__(url)

    @property
    def origin_id(self):
        key = md5(self.url).hexdigest()
        return key

    @property
    def headers(self):
        return self._headers

    @property
    def desc(self):
        _desc = self.soup.select("#productTitle")
        # return _desc[0].string
        if len(_desc):
            return _desc[0].string
        _desc = self.soup.title.string.split(':')
        return _desc[0]

    @property
    def nick(self):
        return 'amazon'

    @property
    def shop_link(self):
        return self.hostname

    @property
    def cid(self):
        cate = self.soup.select("#wayfinding-breadcrumbs_feature_div .a-link-normal")
        # print cate
        if len(cate) > 0:
            href = cate[0].attrs.get('href')
            return href.split('=')[-1]
        return 0

    @property
    def price(self):
        f_price = 0
        pricetag = self.soup.select("#priceblock_ourprice")
        if len(pricetag) > 0:
            # print pricetag[0].string.split('-')
            price = pricetag[0]
            try:
                f_price =  float(price.string[1:].replace(',', ''))
            except UnicodeEncodeError:
                price = pricetag[0].string.split('-')[0]
                f_price = float(price[1:].replace(',', ''))

        pricetag = self.soup.select("#priceblock_saleprice")
        if len(pricetag) > 0:
            price = pricetag[0]
            # print price
            f_price =  float(price.string[1:].replace(',', ''))

        pricetag = self.soup.select("#soldByThirdParty span")
        if len(pricetag) > 0:
            price = pricetag[0].string
            f_price =  float(price[1:])

        if 'amazon.co.jp' in self.hostname:
            f_price = f_price / 20.

        return f_price
        # pricetage = self.soup.select("#paperback_meta_binding_winner")
        # print pricetag

    @property
    def url(self):
        url = "http://%s%s" % (self.urlobj.hostname, self.urlobj.path)
        if 'ref' in url:
            url = urljoin(url, ' ')
        url = url.rstrip()
        match = re.search('\/$', url)
        if match is None:
            url += '/'
        return url

    @property
    def images(self):
        images = list()
        optimages = self.soup.select("#altImages ul .a-list-item span img")
        # return opt
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                if len(img_link) == 0:
                    continue
                array = img_link.split('_')
                res =  "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images

        optimages = self.soup.select("#imageBlockThumbs div img")
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                if len(img_link) == 0:
                    continue
                array = img_link.split('_')
                res =  "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images

        optimages = self.soup.select("#main-image")
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                array = img_link.split('_')
                res =  "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images

        # amazon jp
        # optimages = self.soup.select("#altImages .a-spacing-small ")
        # print optimages


    @property
    def brand(self):
        optbrands = self.soup.select('#brandByline_feature_div div a')
        try:
            brand = optbrands[0].string
            return brand
        except IndexError:
            return ''

if __name__=="__main__":

    a = Amazon("http://www.amazon.co.jp/%E3%83%95%E3%82%A3%E3%83%AA%E3%83%83%E3%83%97%E3%82%B9-%E5%85%89%E7%BE%8E%E5%AE%B9%E5%99%A8-%E3%82%A8%E3%83%83%E3%82%BB%E3%83%B3%E3%82%B7%E3%83%A3%E3%83%AB-SC1991-00/dp/B00SB014CE")
    print a.hostname
    print a.url
    print a.price
    print a.cid
    print a.images
    # print a.buy_link
    print a.desc
    print a.price, a.images
    print a.desc


