from django.http import HttpResponse
from django.utils.log import getLogger

# from wand.image import  Image as WandImage
from django.core.files.storage import default_storage
from apps.core.utils.image import HandleImage
# from django.utils.

log = getLogger('django')


def images(request, file_name, size=None):
    # log.info(size)
    # size = request.GET.get('s', None)
    image_name = 'images/' + file_name

    f = default_storage.open(image_name)
    # log.info(f.read())

    if size is not None:
        image = HandleImage(f)
        _size = float(size)
        image.resize(_size, _size)
        image_data = image.image_data
    else:
        image_data = f.read()

    return HttpResponse(image_data, content_type='image/jpeg')

__author__ = 'edison'
