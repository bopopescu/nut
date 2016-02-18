from django.db import  models
from django.conf import settings
image_host = getattr(settings, 'IMAGE_HOST', None)


class UrlQrcode(models.Model):
    url  = models.CharField(max_length=511)
    url_hash = models.CharField(max_length=255, db_index=True)
    qrCodeImg = models.CharField(max_length=511)

    @property
    def qrCodeImg_url(self):
        return '%s%s' %(image_host, self.qrCodeImg)

