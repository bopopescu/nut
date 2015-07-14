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
        pricetag = self.soup.select("#priceblock_ourprice")
        if len(pricetag) > 0:
            # print pricetag[0].string.split('-')
            price = pricetag[0]
            try:
                return float(price.string[1:].replace(',', ''))
            except UnicodeEncodeError:
                price = pricetag[0].string.split('-')[0]
                return float(price[1:].replace(',', ''))

        pricetag = self.soup.select("#priceblock_saleprice")
        if len(pricetag) > 0:
            price = pricetag[0]
            # print price
            return float(price.string[1:].replace(',', ''))

        pricetag = self.soup.select("#soldByThirdParty span")
        if len(pricetag) > 0:
            price = pricetag[0].string
            return float(price[1:])

        return 0
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
        # print pattern.match(url)
        # m =re.search('\/\Z', url)
        # print m.group(0)
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

    @property
    def brand(self):
        optbrands = self.soup.select('#brandByline_feature_div div a')
        try:
            brand = optbrands[0].string
            return brand
        except IndexError:
            return ''

if __name__=="__main__":

    a = Amazon("http://www.amazon.cn/gp/product/B00LF5DUA6/ref=s9_cngwdyfloorv2-s9?pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=center-2&pf_rd_r=0KJF7YH4D252JM4ZPJKC&pf_rd_t=101&pf_rd_p=252512872&pf_rd_i=899254051")
    print a.url
    print a.price
    print a.cid
    print a.images
    # print a.buy_link
    # print a.desc
    # print a.price, a.images
    # print b.desc


