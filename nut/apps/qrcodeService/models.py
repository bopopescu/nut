from django.db import  models
from django.conf import settings


class UrlQrcode(models.Model):
    url  = models.CharField(max_length=511, required=True)
    url_hash = models.CharField(max_length=255, required=True, db_index=True)
    qrCodeImg = models.CharField(max_length=511,required=True)

    @property
    def qrCodeImg_url(self):
        return '%s%s' %()

