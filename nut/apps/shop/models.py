# coding=utf-8

from django.conf import settings
from django.db import models
from apps.core.models import BaseModel, \
                             GKUser
from apps.banners.models import BaseBanner


from django.utils.translation import ugettext_lazy as _


class StorePageBanners(BaseBanner):
    banner_title = models.CharField(max_length=128, null=True, blank=True)
    banner_desc  = models.CharField(max_length=128, null=True, blank=True)
    pass

class StorePageRecommend(BaseBanner):
    pass


class Shop(BaseModel):
    '''
    ONLY SUPPORT TAOBAO SHOP NOW !!!

    '''
    (other_style, dress, home, culture, sport, tec, food, mother, cosmetic, health) = range(10)
    SHOP_STYLE_CHOICES = [
        (other_style , '其他'),
        (dress,'服饰'),
        (home , '居家'),
        (culture, '文化'),
        (sport, '运动'),
        (tec, '科技'),
        (food,'美食'),
        (mother, '孕婴'),
        (cosmetic,'美容'),
        (health,'健康')
    ]

    (other, taobao, tmall, glbuy, tinter, jiyoujia) = range(6)
    SHOP_TYPE_CHOICES = [
        (other , '其他'),
        (taobao, '淘宝'),
        (tmall , '天猫'),
        (glbuy, '全球购'),
        (tinter, '天猫国际'),
    ]

    owner = models.ForeignKey(GKUser, related_name='shops')
    shop_title = models.CharField(max_length=255)
    shop_link = models.URLField(max_length=255)
    shop_style = models.IntegerField(choices=SHOP_STYLE_CHOICES, default=dress )
    shop_type = models.IntegerField(choices=SHOP_TYPE_CHOICES, default=taobao)
    tb_shop_id = models.CharField(max_length=64, null=True, blank=True)
    common_shop_link = models.CharField(max_length=255, null=True, blank=True)

    @property
    def tb_shop_link(self):
        return 'https://shop%s.taobao.com'%self.tb_shop_id

    def __unicode__(self):
        return '%s:%s'%(self.owner, self.shop_title)