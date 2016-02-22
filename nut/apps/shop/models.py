# coding=utf-8

from django.conf import settings
from django.db import models
from apps.core.models import BaseModel, \
                             GKUser


class Shop(BaseModel):
    owner = models.ForeignKey(GKUser, related_name='shops')
    shop_title = models.CharField(max_length=255)
    shop_link = models.URLField(max_length=255)