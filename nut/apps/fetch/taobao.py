# -*- coding: utf-8 -*-

import re

from urllib import unquote
from django.utils.log import getLogger

from apps.fetch.base import BaseFetcher

IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"
log = getLogger('django')


class TaoBao(BaseFetcher):
    def __init__(self, entity_url):
        BaseFetcher.__init__(self, entity_url)
        self.high_resolution_pattern = re.compile('hiRes"[\s]*:[\s]*"([^";]+)')
        self.large_resolution_pattern = re.compile('large"[\s]*:[\s]*"([^";]+)')
        self.price_pattern = re.compile(u'(?:￥|\$)\s?(?P<price>\d+\.\d+)')
        self.foreign_price = 0.0
        self.entity_url = entity_url
        self.origin_id = self.get_origin_id()
        self.expected_element = 'ul.tb-promo-meta'
        self.shop_link = self.hostname
        self.shop_nick = self.get_nick()

    def get_origin_id(self):
        params = self.entity_url.split("?")[1]
        for param in params.split("&"):
            tokens = param.split("=")
            if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
                return tokens[1]
        # url = unquote_plus(url)
        # params = url.split("?")[1]
        # for param in params.split("&"):
        #     tokens = param.split("=")
        #     if len(tokens) >= 2 and (tokens[0] == "id"
        #                              or tokens[0] == "item_id"
        #                              or tokens[1] == 'itemid'):
        #         return tokens[-1]

    @property
    def link(self):
        link = 'http://item.taobao.com/item.htm?id=%s' % self.origin_id
        return link

    @property
    def nick(self):
        nick = self.soup.select("a.tb-seller-name")
        if nick:
            nick = nick[0].text.strip()
            self._nick = nick
            return nick
        if nick:
            self._nick = nick
            return nick
        nick = self.soup.select(".tb-shop-seller a")
        if nick:
            self._nick = nick[0].text
            return nick[0].text
        try:
            return unquote(self._nick)
        except:
            return ''

    @property
    def cid(self):
        cat = self.headers.get('X-Category')
        try:
            _cid = cat.split('/')
            return _cid[-1]
        except AttributeError, e:
            log.error("Error: %s", e.message)
        return 0

    @property
    def desc(self):
        return self.soup.title.string[0:-4]

    @property
    def price(self):
        price_tag = self.get_price_tag()
        if not price_tag:
            return 0.0
        if price_tag:
            price_string = re.findall("\d+\.\d+", price_tag)
            if price_string:
                return float(price_string[0])
            else:
                return 0.0

    def get_price_tag(self):
        price_tag_names = (
            '#J_PromoPriceNum',
            'span.tb-promo-price',
            'em.tb-rmb-num',
            'strong.tb-rmb-num',
            'span.originPrice',
        )
        for price_tag_name in price_tag_names:
            price_tags = self.soup.select(price_tag_name)
            if len(price_tags) > 0:
                for price_tag in price_tags:
                    if price_tag.text:
                        return price_tag.text

    @property
    def images(self):
        _images = list()
        fimg = self.soup.select("#J_ImgBooth")
        if not fimg:
            fimg = self.soup.select("#J_ThumbContent img")

        fjpg = fimg[0].attrs.get('data-src')
        if not fjpg:
            fjpg = fimg[0].attrs.get('src')

        fjpg = re.sub(IMG_POSTFIX, "", fjpg)

        if "http" not in fjpg:
            fjpg = "http:" + fjpg
        _images.append(fjpg)

        optimgs = self.soup.select("ul#J_UlThumb li a img")

        for op in optimgs:
            try:
                optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
            except TypeError:
                optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('data-src'))
            if "http" not in optimg:
                optimg = "http:" + optimg
            if optimg in _images:
                continue
            _images.append(optimg)
        return _images

    @property
    def shoplink(self):
        shopidtag = re.findall('shopId:"(\d+)', self.html)
        if len(shopidtag) > 0:
            return "http://shop" + shopidtag[0] + ".taobao.com"
        shopidtag = self.soup.select("div.tb-shop-info-ft a")
        if shopidtag:
            shop_link = shopidtag[0].attrs.get('href')
            if shop_link.startswith('//'):
                shop_link = shop_link[2:]
            return shop_link
        shopidtag = tb_shop_name = self.soup.select("div.tb-shop-name a")
        if shopidtag:
            return tb_shop_name[0].attrs.get('href')
        return "http://chaoshi.tmall.com/"

    @property
    def brand(self):
        seller_soup = self.soup.select("ul.attributes-list li")
        if not seller_soup:
            seller_soup = self.soup.select("ul#J_AttrUL li")
        if seller_soup > 0:
            for brand_li in seller_soup:
                if brand_li.text.find(u'品牌') >= 0:
                    return brand_li.text.split(u':')[1].strip()

    def get_nick(self):
        pass
