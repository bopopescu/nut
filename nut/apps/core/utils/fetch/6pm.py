from spider import Spider
from hashlib import md5

class SixPM(Spider):

    def __init__(self, url):
        super(SixPM, self).__init__(url)


    @property
    def origin_id(self):
        key = md5(self.url).hexdigest()
        return key

    @property
    def nick(self):
        return '6pm'

    @property
    def brand(self):
        brand = self.soup.select("#productStage h1 .brand")
        return brand[0].string

    @property
    def desc(self):
        desc = self.soup.select("#productStage h1 .link fn")
        return desc[0].string

    @property
    def price(self):
        pricetag = self.soup.select("#priceSlot .price")
        price = pricetag[0].string.replace('$', '')
        return round(float(price) * 6.2, 2)

    @property
    def images(self):
        images = list()
        optimages = self.soup.select("#productImages ul li a span img")
        if len(optimages) > 0:
            for row in optimages:
                image = row.attrs.get('src')
                # print image
                images.append(image)
        return images
        # print optimages


if __name__=="__main__":

    pm = SixPM("http://www.6pm.com/michael-antonio-avalon-brown")
    print pm.price

__author__ = 'edison'
