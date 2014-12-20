from django.http import HttpResponse, Http404
from django.utils.log import getLogger

from apps.images.tasks import resize
# from wand.image import  Image as WandImage
# from django.core.files.storage import default_storage
# from apps.core.utils.image import HandleImage

# from django.utils.

log = getLogger('django')


def images(request, file_name, size=None):
    path = request.get_full_path()
    path = path.split('/')
    log.info(path)
    image_name = "%s/%s" % (path[1], path[-1])

    result = resize.apply_async((image_name, size), expires=60)
    image_data = result.get()

    if image_data:
        return HttpResponse(image_data, content_type='image/jpeg')
    raise Http404




__author__ = 'edison'
