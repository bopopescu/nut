# -*- coding: utf-8 -*-

from urlparse import urljoin
from hashlib import md5
import re

from django.conf import settings

from apps.core.utils.fetch.spider import Spider
from apps.core.utils.commons import currency_converting
from settings import CURRENCY_SYMBOLS


class Amazon(Spider):
    def __init__(self, url):
        self.high_resolution_pattern = re.compile('hiRes"[\s]*:[\s]*"([^";]+)')
        self.large_resolution_pattern = re.compile('large"[\s]*:[\s]*"([^";]+)')
        self.price_pattern = re.compile(u'(?:￥|\$)\s?(?P<price>\d+\.\d+)')
        self.foreign_price = None
        super(Amazon, self).__init__(url)

    @property
    def origin_id(self):
        key = md5(self.url).hexdigest()
        # print "url %s" % self.url
        # m =  re.search(r"gp\/product\/(\w+)\/?", self.url)
        # print m.group(1)
        return key

    @property
    def headers(self):
        return self._headers

    @property
    def desc(self):
        _desc = self.soup.select("#productTitle")
        # return _desc[0].string
        if len(_desc):
            return _desc[0].string.strip()
        _desc = self.soup.title.string.split(':')
        return _desc[0].strip()

    @property
    def nick(self):
        return 'amazon'

    @property
    def shop_link(self):
        return self.hostname

    @property
    def cid(self):
        cate = self.soup.select(
            "#wayfinding-breadcrumbs_feature_div .a-link-normal")
        # print '>>> cate: ',  cate
        if len(cate) > 0:
            href = cate[0].attrs.get('href')
            return href.split('=')[-1]
        return 0

    @property
    def price(self):
        f_price = self.get_price_tag()
        if not f_price:
            return 0.0

        if not self.hostname.endswith('.cn'):
            cny_price = 0
            self.foreign_price = f_price
            if self.hostname.endswith('.com'):
                cny_price = currency_converting('USD', f_price)
            elif self.hostname.endswith('.jp'):
                cny_price = currency_converting('JPY', f_price)
            return cny_price
        return f_price

    def get_price_tag(self):
        f_price = 0
        pricetag = self.soup.select("#priceblock_dealprice")
        if len(pricetag) > 0:
            price = pricetag[0]
            f_price = float(price.string[1:].replace(',', ''))
            return f_price

        pricetag = self.soup.select("#priceblock_ourprice")
        if len(pricetag) > 0:
            price = pricetag[0].string
            if price.find('-') >= 0:
                price = price.split('-')[1].strip()
            f_price = float(price[1:].replace(',', ''))
            return f_price

        pricetag = self.soup.select("#priceblock_saleprice")
        if len(pricetag) > 0:
            price = pricetag[0]
            f_price = float(price.string[1:].replace(',', ''))
            return f_price

        pricetag = self.soup.select("#soldByThirdParty span")
        if len(pricetag) > 0:
            price = 0
            for tag in pricetag:
                if tag.string.startswith(CURRENCY_SYMBOLS):
                    price = tag.string
            price = price.strip()
            f_price = float(price[1:].replace(',', ''))
            return f_price

        pricetag = self.soup.select("div#tmmSwatches ul")
        if len(pricetag) > 0:
            prices = self.price_pattern.findall(pricetag[0].text,
                                                re.MULTILINE)
            if len(prices) == 1:
                return prices[0]
            prices = [float(price) for price in prices]
            prices.sort()
            return prices[0]

        pricetag = self.soup.select("span#ags_price_local")
        if len(pricetag) > 0:
            price = pricetag[0].string
            price = price.strip()
            f_price = float(price[1:].replace(',', ''))
            return f_price

        pricetag = self.soup.select("table.product")
        if len(pricetag) > 0:
            prices = self.price_pattern.findall(pricetag[0].text,
                                                re.MULTILINE)
            if len(prices) == 1:
                return prices[0]
            prices = [float(price) for price in prices]
            prices.sort()
            return prices[0]
        return f_price

    @property
    def url(self):
        try:
            short_path = re.findall(r'(/(dp|gp)/\w{10})', self.urlobj.path)[0][0]
            url = "http://%s%s" % (self.urlobj.hostname, short_path)
        except:
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
        images = []
        image_js = self.soup.select("div#imageBlock_feature_div")
        if image_js:
            hires_images = self.high_resolution_pattern.findall(
                image_js[0].text)
            if hires_images:
                images = hires_images
            else:
                large_images = self.large_resolution_pattern.findall(
                    image_js[0].text)
                if large_images:
                    images = large_images
        else:
            images = self.get_medium_images()
        if not images:
            try:
                images = self.soup.select("img#imgBlkFront")[0]['data-a-dynamic-image']
                images = [re.findall(r'(http.+?\.jpg)', images)[0]]
            except:
                images = [urljoin(settings.IMAGE_HOST, 'images/8c19d8cef88c36b0511c1b217512174d.jpeg')]
        return images

    def get_medium_images(self):
        images = list()
        optimages = self.soup.select("#altImages ul .a-list-item span img")
        # return opt
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                if len(img_link) == 0:
                    continue
                array = img_link.split('_')
                res = "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images

        optimages = self.soup.select("#imageBlockThumbs div img")
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                if len(img_link) == 0:
                    continue
                array = img_link.split('_')
                res = "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images

        optimages = self.soup.select("#main-image")
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                array = img_link.split('_')
                res = "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images
        # TODO : handle can not find image error

        return []

            # amazon jp
            # optimages = self.soup.select("#altImages .a-spacing-small ")
            # print optimages


    @property
    def brand(self):
        optbrands = self.soup.select('#brandByline_feature_div div a')
        if optbrands:
            try:
                brand = optbrands[0].string
                return brand.strip()
            except IndexError:
                return ''
        else:
            another_try = self.soup.select("a#brand")
            if another_try:
                return another_try[0].strip()


if __name__ == "__main__":
    # a = Amazon("http://www.amazon.co.jp/%E3%83%95%E3%82%A3%E3%83%AA%E3%83%83%E3%83%97%E3%82%B9-%E5%85%89%E7%BE%8E%E5%AE%B9%E5%99%A8-%E3%82%A8%E3%83%83%E3%82%BB%E3%83%B3%E3%82%B7%E3%83%A3%E3%83%AB-SC1991-00/dp/B00SB014CE")
    a = Amazon(
        "http://www.amazon.cn/Borghese%E8%B4%9D%E4%BD%B3%E6%96%AF%E6%B4%BB%E5%8A%9B%E4%BA%AE%E9%87%87%E7%BE%8E%E8%82%A4%E6%B3%A5%E6%B5%86%E9%9D%A2%E8%86%9C430ml/dp/B00554AJ02")
    print a.hostname
    print a.url
    print a.price
    print a.cid
    print a.images
    # print a.buy_link
    print a.desc
    print a.price, a.images
    print a.desc


