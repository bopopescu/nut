# -*- coding: utf-8 -*-

import re

from django.utils.log import getLogger

from apps.fetch.base import BaseFetcher


IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"
log = getLogger('django')


class TaoBao(BaseFetcher):
    def __init__(self, entity_url):
        BaseFetcher.__init__(self, entity_url)
        self.nick_pattern = re.compile(u'掌\s+柜：(?P<nick>.*)',
                                       re.MULTILINE | re.UNICODE)
        self.cid_pattern = re.compile(u'cid\s+:\s+(?P<cid>)\d*')
        self.foreign_price = 0.0
        self.entity_url = entity_url
        self.origin_id = self.get_origin_id()
        self.expected_element = 'ul.tb-promo-meta'

    def get_origin_id(self):
        params = self.entity_url.split("?")[1]
        for param in params.split("&"):
            tokens = param.split("=")
            if len(tokens) >= 2 and (tokens[0] == "id" or
                                     tokens[0] == "item_id" or
                                     tokens[1] == 'itemid'):
                return tokens[-1]

    @property
    def link(self):
        link = 'http://item.taobao.com/item.htm?id=%s' % self.origin_id
        return link

    @property
    def shop_nick(self):
        nick = self.soup.select("a.tb-seller-name")
        if nick:
            nick = nick[0].text.strip()
            return nick
        if nick:
            return nick

        nick = self.soup.select(".tb-shop-seller a")
        if nick:
            return nick[0].text

        nick_tag = self.soup.select("div.shop-more-info")
        if nick_tag:
            nick = self.nick_pattern.findall(nick_tag[0].text)
            if nick:
                return nick[0]
        return ''

    @property
    def cid(self):
        cid_tags = ('div#detail-recommend-bought',
                    'div#J_Pine',
                    'div#detail-recommend-viewed')
        for cid_tag_name in cid_tags:
            cid_tag = self.soup.select(cid_tag_name)
            if cid_tag:
                return cid_tag[0].attrs['data-catid']
        return ''

    @property
    def title(self):
        return self.soup.title.string[0:-4]

    @property
    def price(self):
        price_tag = self._get_price_tag()
        if not price_tag:
            return 0.0
        if price_tag:
            price_string = re.findall("\d+\.\d+", price_tag)
            if price_string:
                return float(price_string[0])
            else:
                return 0.0

    def _get_price_tag(self):
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
        img_tags = self.soup.select("#J_ImgBooth")
        if not img_tags:
            img_tags = self.soup.select("#J_ThumbContent img")

        fjpg = img_tags[0].attrs.get('data-src')
        if not fjpg:
            fjpg = img_tags[0].attrs.get('src')

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
    def shop_link(self):
        shop_id_tag = re.findall('shopId:"(\d+)', self.html_source)
        if len(shop_id_tag) > 0:
            return "http://shop" + shop_id_tag[0] + ".taobao.com"

        shop_id_tag = self.soup.select("div.tb-shop-info-ft a")
        if shop_id_tag:
            shop_link = shop_id_tag[0].attrs.get('href')
            if shop_link.startswith('//'):
                shop_link = shop_link[2:]
            return shop_link

        shop_id_tag = tb_shop_name = self.soup.select("div.tb-shop-name a")
        if shop_id_tag:
            return tb_shop_name[0].attrs.get('href')

        shop_id_tag = self.soup.select('a.shop-entry')
        if shop_id_tag:
            shop_link = shop_id_tag[0].attrs.get('href')
            if shop_link.startswith('//'):
                shop_link = shop_link[2:]
            return shop_link
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
