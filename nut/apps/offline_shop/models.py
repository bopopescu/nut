from django.core.urlresolvers import reverse
from django.db import models
from apps.core.base import BaseModel
from apps.core.models import GKUser
from apps.core.extend.fields.listfield import ListObjectField
from apps.order.models import SKU
from django.conf import settings


class Offline_Shop_Info_Manager(models.Manager):
    def active_offline_shops(self):
        return self.filter(status=True).order_by('position')


class Offline_Shop_Info(BaseModel):
    # one to one relation to GKUser
    shop_owner = models.OneToOneField(GKUser, related_name='offline_shop')

    shop_name = models.CharField(max_length=64, null=True, blank=True)
    shop_desc = models.TextField(null=True, blank=True)
    shop_address = models.CharField(max_length=256, null=True, blank=True)
    shop_opentime = models.CharField(max_length=256, null=True, blank=True)

    # float baidu map lng and lat
    address_lng = models.FloatField(null=True, db_index=True)
    address_lat = models.FloatField(null=True, db_index=True)

    images = ListObjectField(null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)

    shop_tel = models.CharField(max_length=32, null=True, blank=True)
    shop_mobile = models.CharField(max_length=32, null=True, blank=True)

    status = models.BooleanField(default=True)
    position = models.IntegerField(default=0)

    objects = Offline_Shop_Info_Manager()

    class Meta:
        ordering = ['position']

    @property
    def mobile_url(self):
        return 'http://m.guoku.com'+reverse('web_offline_shop_detail',
                                            args=[self.pk])

    def cover_url(self):
        if self.images:
            return self.images[0]
        else:
            return "%s%s" % (settings.STATIC_URL, 'images/article/default_cover.jpg')


class Shop_SKU_Stock(models.Model):

    shop = models.ForeignKey(Offline_Shop_Info, on_delete=models.PROTECT)
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT)
    stock = models.IntegerField(default=0)
    # origin price is not include Shop_SKU_stock
    discount = models.FloatField(default=1, db_index=True)
    promo_price = models.FloatField(default=0, db_index=True)

    @property
    def origin_price(self):
        return self.sku.origin_price

    def get_discount_rate(self):
        if self.origin_price == 0  or self.promo_price == 0 :
            return 1
        return self.promo_price/(self.origin_price*1.0)

    def save(self, *args, **kwargs):
        self.discount = self.get_discount_rate()
        # self.entity.updated_time = datetime.now()
        # self.entity.save()
        super(SKU, self).save(*args, **kwargs)
