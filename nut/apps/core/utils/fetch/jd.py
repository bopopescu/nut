#encoding=utf8

import urllib2 
from bs4 import BeautifulSoup
import re 
import json

class JDExtractor:
    
    @staticmethod
    def fetch_item(itemid):
        link = ""
        if type(itemid) == int:
            link = "http://item.jd.com/%d.html"%itemid
        else:
            link = "http://item.jd.com/%s.html"%itemid
        resp = urllib2.urlopen(link)
        
        html = resp.read()
        # html = html.decode("gbk").encode("utf8")

        return JDExtractor.parser(html, itemid)

    @staticmethod
    def parser(html, itemid):
        soup = BeautifulSoup(html, from_encoding="gb18030")

        title = soup.title.string
        title = title[:-18]
        
        imgtags = soup.select("html body div.w div#product-intro \
                div#preview div#spec-list div.spec-items ul li img")
        imgs = []

        for tag in imgtags:
            src = tag['src']
            src = src.replace('com/n5','com/n1')
            imgs.append(src)
        
        cattag = soup.select("html body div.w div.breadcrumb span a")[1]
        catlink = cattag.attrs['href']
        catstr = re.findall(r'\d+',catlink)
        category = [int(x) for x in catstr]

        tmp = re.findall(r'店铺.*>(.+)</a>',html)
        nick = ""
        shop_link = ""
        if len(tmp)>0:
            nick = tmp[0]
            link = re.findall(r'店铺.* href="(.+)">',html)[0]
            shop_link = link[:-16]
        else:
            nick="京东"
            shop_link = "http://jd.com"
        itemid = int(itemid)
        price_link = "http://p.3.cn/prices/get?skuid=J_%d&type=1&area=1_72_4137&callback=cnp"%itemid
        resp = urllib2.urlopen(price_link)
        data = resp.read()
        data = data[5:-4]
        pj = json.loads(data)
        price = float(pj['p'])
        
        brandtag = soup.select("ul.detail-list li a")
        brand = ""
        if len(brandtag)>0:
            brand = brandtag[0].string
            brand = brand.replace(u"旗舰店","")
            brand = brand.replace(u"官方","")
        result = {
            "desc" : title,
            "price" : price,
            "category" : category,
            "imgs" : imgs,
            "nick" : nick,
            "brand": brand,
            'cid' : '',
            "shop_link" : shop_link
        }

        return result

if __name__ == '__main__':
    jd = JDExtractor()

    result = jd.fetch_item(210347)

    print result
