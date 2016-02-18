from apps.qrcodeService.models import UrlQrcode
from apps.core.utils.image import HandleImage
from django.core.files.storage import default_storage
from django.conf import  settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')

import hashlib
import qrcode


def createQrImage(url):
    qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=1
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    return img

def getQrImageFileName(url):
    return '%sqr_%s.png' % (image_path,getUrlHash(url))

def createQrcodeItem(url):
    qrImage = createQrImage(url)
    fileName = getQrImageFileName(url)
    fd = default_storage.open(fileName, 'w')
    qrImage.save(fd )
    urlQrcodeItem  = UrlQrcode.objects.create(url=url, url_hash=getUrlHash(url), qrCodeImg=fileName)
    urlQrcodeItem.save()
    return urlQrcodeItem

def getUrlHash(url):
    return hashlib.sha1(url).hexdigest()

def get_qrcode_img_url(url):
    hash = getUrlHash(url)
    try:
        qrcode =UrlQrcode.objects.get(url_hash=hash)
    except UrlQrcode.DoesNotExist as e :
        qrcode = createQrcodeItem(url)

    except UrlQrcode.MultipleObjectsReturned:
        raise  Exception('hash collision in urlQrcode')
        return None

    return qrcode.qrCodeImg_url

if __name__ == '__main__':
    pass
    # createQrcodeItem('http://127.0.0.1:9766/')



