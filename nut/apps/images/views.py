from django.http import HttpResponse
from django.utils.log import getLogger

from apps.images.tasks import resize
# from wand.image import  Image as WandImage
# from django.core.files.storage import default_storage
# from apps.core.utils.image import HandleImage

# from django.utils.

log = getLogger('django')


def images(request, file_name, size=None):
    # log.info(request.get_full_path())
    # size = request.GET.get('s', None)
    path = request.get_full_path()
    path = path.split('/')
    log.info(path)
    image_name = "%s/%s" % (path[1], path[-1])

    # f = default_storage.open(image_name)
    # # log.info(f.read())
    #
    # if size is not None:
    #     image = HandleImage(f)
    #     _size = float(size)
    #     image.resize(_size, _size)
    #     image_data = image.image_data
    # else:
    #     image_data = f.read()

    result = resize.apply_async((image_name, size))
    image_data = result.get()
    return HttpResponse(image_data, content_type='image/jpeg')

__author__ = 'edison'
