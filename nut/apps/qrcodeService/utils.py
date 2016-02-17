from apps.qrcodeService.models import UrlQrcode
from apps.core.utils.image import HandleImage

import hashlib
import qrcode


def createQrcodeItem(url):
    qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=1
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    gkImg  = HandleImage(img)
    imgPath = gkImg.save()

    urlimg  = UrlQrcode.objects.create(url=url, url_hash=getUrlHash(url), qrCodeImg=imgPath)
    urlimg.save()
    return urlimg


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

    return qrcode.qrCodeImg




