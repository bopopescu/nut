# coding=utf-8

from django.conf import settings
from django.db import models
from apps.core.models import BaseModel, \
                             GKUser

from django.utils.translation import ugettext_lazy as _


class Shop(BaseModel):
    (delicacy, culture, looks, lifestyle) = range(4)
    SHOP_STYLE_CHOICES = [
        (delicacy , '美味佳肴'),
        (culture , '文艺漫游'),
        (looks, '衣衫配饰'),
        (lifestyle, '生活榜样')
    ]

    (other, taobao, tmall, glbuy) = range(4)
    SHOP_TYPE_CHOICES = [
        (other , '其他'),
        (taobao, '淘宝'),
        (tmall , '天猫'),
        (glbuy, '全球购')
    ]


    owner = models.ForeignKey(GKUser, related_name='shops')
    shop_title = models.CharField(max_length=255)
    shop_link = models.URLField(max_length=255)
    shop_style = models.IntegerField(choices=SHOP_STYLE_CHOICES, default=delicacy )
    shop_type = models.IntegerField(choices=SHOP_TYPE_CHOICES, default= taobao)
