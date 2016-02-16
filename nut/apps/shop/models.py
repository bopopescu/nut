# coding=utf-8

from django.conf import settings
from django.db import models
from apps.core.models import BaseModel, \
                             GKUser


class Shop(BaseModel):
    seller = models.ForeignKey(GKUser, related_name='shops')
    shop_title = models.CharField(max_length=255, db_index=True)
    shop_link = models.URLField(max_length=255)
    shop_desc = models.CharField(max_length=511)
    pass