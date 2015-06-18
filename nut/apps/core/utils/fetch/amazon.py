# -*- coding: utf-8 -*-

from apps.core.utils.fetch.spider import Spider


class Amazon(Spider):

    def __init__(self, url):
        super(Amazon, self).__init__(url)

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
        price = pricetag[0]
        return float(price.string[1:].replace(',', ''))

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

    a = Amazon("http://www.amazon.cn/gp/product/B00BVV0VQU/ref=s9_cngwdyfloorv2-s9?pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=center-2&pf_rd_r=0DEMD1RDSC5AD4HC9KWA&pf_rd_t=101&pf_rd_p=251248392&pf_rd_i=899254051")
    print a.brand
    print a.buy_link
    # print a.desc
    # print a.price, a.images
    # print b.desc


