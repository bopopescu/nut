# coding=utf-8
from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _
from apps.core.models import BaseModel, GKUser, Article


image_host = getattr(settings, 'IMAGE_HOST', None)

class Seller_Profile_Queryset(models.query.QuerySet):
    def active_seller(self):
        return self.filter(status=1)

    def seller_2016(self):
        return self.filter(is2016store=True)

    def seller_2015(self):
        return self.filter(is2015store=True)

    def ordered_profile(self):
        return self.extra(select={'converted_title': 'CONVERT(shop_title USING gbk)'},
                          order_by=['converted_title'])

    def ordered_all_profile(self):
        return self.extra(select={'converted_title': 'CONVERT(shop_title USING gbk)'},
                          order_by=['-gk_stars','converted_title'])


class Seller_Profile_Manager(models.Manager):

    def get_queryset(self):
        return Seller_Profile_Queryset(self.model, using = self._db)

    def active_seller(self):
        return self.get_queryset().filter(status=1)

    def seller_2016(self):
        return self.get_queryset().seller_2016()

    def seller_2015(self):
        return self.get_queryset().seller_2015()

    def ordered_profile(self):
        return self.get_queryset().ordered_profile()

    def ordered_all_profile(self):
        return self.get_queryset().ordered_all_profile()




class Seller_Profile(BaseModel):
    (active,deactive) = (1,0)

    SELLER_STATUS_CHOICE=[(active,"正常卖家"),(deactive, "冻结卖家")]

    (blank ,cloth, culture, food, life) = (0,1,2,3,4)

    BUS_SECTION_CHOICE = [
        (blank, "空白"),
        (cloth, "服饰"),
        (culture,"文化"),
        (food,"美食"),
        (life,"生活")
    ]

    GKSTAR_CHOICE=[
                (1, "1星"),
                (2, "2星"),
                (3, "3星"),
                (4, "4星"),
                (5, "5星"),
            ]

    user = models.OneToOneField(GKUser, related_name='seller_profile', null=True)
    shop_title = models.CharField(max_length=255, db_index=True)
    shop_link = models.URLField(max_length=255)
    seller_name = models.CharField(max_length=255, db_index=True)
    shop_desc = models.TextField(max_length=255)
    status = models.IntegerField(choices=SELLER_STATUS_CHOICE, default=active)
    logo = models.CharField(max_length=255, blank=True)
    category_logo = models.CharField(max_length=255, blank=True)
    business_section = models.IntegerField(choices=BUS_SECTION_CHOICE, default=blank)
    gk_stars = models.IntegerField(choices=GKSTAR_CHOICE, default=5)
    related_article = models.OneToOneField(Article, related_name='related_seller',null=True, blank=True)
    is2016store = models.BooleanField(default=True)
    is2015store = models.BooleanField(default=True)

    objects = Seller_Profile_Manager()

    def __unicode__(self):
        return '%s_%s' %(self.seller_name, self.shop_title)

    @property
    def logo_url(self):
        return '%s%s' %(image_host, self.logo)

    @property
    def category_logo_url(self):
        return '%s%s' %(image_host, self.category_logo)
