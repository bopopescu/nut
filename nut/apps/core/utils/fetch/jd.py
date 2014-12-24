#encoding=utf8

import urllib2 
from bs4 import BeautifulSoup
import re 
import json


class JD():

    def __init__(self, item_id):
        self.item_id = item_id
        self.html = self.fetch_html()
        self.soup = BeautifulSoup(self.html, from_encoding="gb18030")

        self.price_json = self.fetch_price()
        # self.price_link = "http://p.3.cn/prices/get?skuid=J_%d&type=1&area=1_72_4137&callback=cnp" % self.item_id

    def fetch_html(self):
        try:
            f = urllib2.urlopen('http://item.jd.com/%s.html' % self.item_id)
        except Exception, e:
            raise

        self._headers = f.headers
        return f.read()

    def fetch_price(self):
        price_link = "http://p.3.cn/prices/get?skuid=J_%s&type=1&area=1_72_4137&callback=cnp" % self.item_id
        resp = urllib2.urlopen(price_link)
        data = resp.read()
        data = data[5:-4]
        # pj = json.loads(data)
        return json.loads(data)

    @property
    def title(self):
        self._title = self.soup.title.string
        # print self._title
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

    @property
    def shop_link(self):
        tmp = re.findall(r'店铺.*>(.+)</a>', self.html)
        shop_link = ""
        if len(tmp)>0:
            nick = tmp[0]
            link = re.findall(r'店铺.* href="(.+)">', self.html)[0]
            shop_link = link[:-16]
        else:
            nick="京东"
            shop_link = "http://jd.com"

        return shop_link

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
#         price_link = "http://p.3.cn/prices/get?skuid=J_%d&type=1&area=1_72_4137&callback=cnp"%itemid
#         resp = urllib2.urlopen(price_link)
#         data = resp.read()
#         data = data[5:-4]
#         pj = json.loads(data)
#         price = float(pj['p'])


# class JDExtractor:
#
#     @staticmethod
#     def fetch_item(itemid):
#         link = ""
#         if type(itemid) == int:
#             link = "http://item.jd.com/%d.html"%itemid
#         else:
#             link = "http://item.jd.com/%s.html"%itemid
#         resp = urllib2.urlopen(link)
#
#         html = resp.read()
#         # html = html.decode("gbk").encode("utf8")
#
#         return JDExtractor.parser(html, itemid)
#
#     @staticmethod
#     def parser(html, itemid):
#         soup = BeautifulSoup(html, from_encoding="gb18030")
#
#         title = soup.title.string
#         title = title[:-18]
#
#         imgtags = soup.select("html body div.w div#product-intro \
#                 div#preview div#spec-list div.spec-items ul li img")
#         imgs = []
#
#         for tag in imgtags:
#             src = tag['src']
#             src = src.replace('com/n5','com/n1')
#             imgs.append(src)
#
#         cattag = soup.select("html body div.w div.breadcrumb span a")[1]
#         catlink = cattag.attrs['href']
#         catstr = re.findall(r'\d+',catlink)
#         category = [int(x) for x in catstr]
#
#         tmp = re.findall(r'店铺.*>(.+)</a>',html)
#         nick = ""
#         shop_link = ""
#         if len(tmp)>0:
#             nick = tmp[0]
#             link = re.findall(r'店铺.* href="(.+)">',html)[0]
#             shop_link = link[:-16]
#         else:
#             nick="京东"
#             shop_link = "http://jd.com"
#         itemid = int(itemid)
#         price_link = "http://p.3.cn/prices/get?skuid=J_%d&type=1&area=1_72_4137&callback=cnp"%itemid
#         resp = urllib2.urlopen(price_link)
#         data = resp.read()
#         data = data[5:-4]
#         pj = json.loads(data)
#         price = float(pj['p'])
#
#         brandtag = soup.select("ul.detail-list li a")
#         brand = ""
#         if len(brandtag)>0:
#             brand = brandtag[0].string
#             brand = brand.replace(u"旗舰店","")
#             brand = brand.replace(u"官方","")
#         result = {
#             "desc" : title,
#             "price" : price,
#             "category" : category,
#             "imgs" : imgs,
#             "nick" : nick,
#             "brand": brand,
#             'cid' : '',
#             "shop_link" : shop_link
#         }
#
#         return result
#
if __name__ == '__main__':

    result = JD(210347)

    print result.title
