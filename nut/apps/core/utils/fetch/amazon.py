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
            print price
            return float(price.string[1:].replace(',', ''))

        pricetag = self.soup.select("#soldByThirdParty")
        print pricetag

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

    a = Amazon("http://www.amazon.cn/gp/product/B00ZOTR98S/ref=s9_cngwdyfloorv2-s9?pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=center-2&pf_rd_r=1E361MGCXY8ZKYJBD5C4&pf_rd_t=101&pf_rd_p=252512872&pf_rd_i=899254051")
    print a.url
    # print a.html
    print a.price
    # print a.buy_link
    # print a.desc
    # print a.price, a.images
    # print b.desc


