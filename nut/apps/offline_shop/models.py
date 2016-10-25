from django.db import models
from apps.core.base import BaseModel
from apps.core.models import GKUser
from apps.core.extend.fields.listfield import ListObjectField


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

    status = models.BooleanField(default=False)
    position = models.IntegerField(default=0)

    objects = Offline_Shop_Info_Manager()

    class Meta:
        ordering = ['position']









