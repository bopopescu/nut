from django.http import HttpResponse, Http404
from django.utils.log import getLogger

from apps.images.tasks import resize


log = getLogger('django')


def images(request, file_name, size=None):
    path = request.get_full_path()
    # log.info(path)
    if "/large/" in path or "small" in path:
        path = path.split('/')
        # log.info(path)
        image_name = "%s/%s/%s" % (path[1], path[-2], path[-1])
    else:
        path = path.split('/')
        image_name = "%s/%s" % (path[1], path[-1])

    # log.info(image_name)
    # result = resize.apply_async((image_name, size), expires=15)
    # image_data = result.get()
    image_data = resize(image_name, size)
    # log.info(image_data)
    if image_data:
        return HttpResponse(image_data, content_type='image/jpeg')
    raise Http404


def old_format_images(request, file_name, size=None):
    _size = size.split('x')
    path = request.get_full_path()
    # print path

    if 'avatar' in path:
        image_name = path
        image_data = resize(image_name)
        # result = resize.apply_async((image_name, size=None), expires=5)
    else:
    # log.info(_size)
        path = path.split('_')
    # log.info(path)
        path = path[0].strip('/')
    # log.info(path)
        image_name = path

        result = resize.apply_async((image_name, _size[0]), expires=5)
        image_data = result.get()

    if image_data:
        return HttpResponse(image_data, content_type='image/jpeg')
    raise Http404
    # return HttpResponse("OK")


__author__ = 'edison'
