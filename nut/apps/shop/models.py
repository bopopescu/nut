# coding=utf-8

from django.conf import settings
from django.db import models
from apps.core.models import BaseModel, \
                             GKUser

from django.utils.translation import ugettext_lazy as _


class Shop(BaseModel):
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
        (jiyoujia,'极有家')
    ]


    owner = models.ForeignKey(GKUser, related_name='shops')
    shop_title = models.CharField(max_length=255)
    shop_link = models.URLField(max_length=255)
    shop_style = models.IntegerField(choices=SHOP_STYLE_CHOICES, default=dress )
    shop_type = models.IntegerField(choices=SHOP_TYPE_CHOICES, default= taobao)
