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
            price = pricetag[0]
            return float(price.string[1:].replace(',', ''))

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

    a = Amazon("http://www.amazon.cn/%E5%9B%BE%E7%81%B5%E6%96%B0%E7%9F%A5-%E4%BF%A1%E6%81%AF%E7%AE%80%E5%8F%B2-%E8%A9%B9%E5%A7%86%E6%96%AF%C2%B7%E6%A0%BC%E9%9B%B7%E5%85%8B/dp/B00G6CY2R8/ref=pd_sim_14_4?ie=UTF8&refRID=17WFPQM9QV27GPGHS0PN")
    print a.url
    # print a.html
    print a.images
    # print a.buy_link
    # print a.desc
    # print a.price, a.images
    # print b.desc


