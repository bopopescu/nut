# -*- coding: utf-8 -*-

from apps.core.utils.fetch.spider import Spider
from urlparse import urljoin
from hashlib import md5

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
        return 0

    @property
    def price(self):
        pricetag = self.soup.select("#priceblock_ourprice")
        if len(pricetag) > 0:
            # print pricetag[0].string.split('-')
            price = pricetag[0]
            try:
                return float(price.string[1:].replace(',', ''))
            except UnicodeEncodeError:
                price = pricetag[0].string.split('-')[0]
                return float(price[1:].replace(',', ''))
                # print "OKOKO"


        pricetag = self.soup.select("#priceblock_saleprice")
        if len(pricetag) > 0:
            price = pricetag[0]
            # print price
            return float(price.string[1:].replace(',', ''))
        # price = self.soup.select('.a-color-price')
        # print price

        pricetag = self.soup.select("#soldByThirdParty span")
        if len(pricetag) > 0:
            price = pricetag[0].string
            return float(price[1:])

    @property
    def url(self):
        url = "http://%s%s" % (self.urlobj.hostname, self.urlobj.path)
        if 'ref' in url:
            url = urljoin(url, ' ')
        return url.rstrip()

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

    @property
    def brand(self):
        optbrands = self.soup.select('#brandByline_feature_div div a')
        try:
            brand = optbrands[0].string
            return brand
        except IndexError:
            return ''

if __name__=="__main__":

    a = Amazon("http://www.amazon.cn/Onitsuka-Tiger-%E9%AC%BC%E5%A1%9A%E8%99%8E-%E4%B8%AD%E6%80%A7-%E4%BC%91%E9%97%B2%E8%B7%91%E6%AD%A5%E9%9E%8B-D508N-0144-%E7%99%BD%E8%89%B2-%E8%93%9D%E8%89%B2-37/dp/B00WHBAC3U/ref=sr_1_10?s=shoes&ie=UTF8&qid=1436334446&sr=1-10")
    print a.url
    print a.price
    # print a.html
    print a.images
    # print a.buy_link
    # print a.desc
    # print a.price, a.images
    # print b.desc


