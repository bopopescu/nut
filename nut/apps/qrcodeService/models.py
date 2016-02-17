from django.db import  models

class Qrcodes(models.Model):
    url  = models.CharField(max_length=511, required=True)
    url_hash = models.CharField(max_length=255, required=True)
    qrCodeImg = models.CharField(max_length=511,required=True)

