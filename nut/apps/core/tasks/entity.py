from celery.task import task
from apps.core.tasks import BaseTask

import urllib2
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from apps.core.utils.image import HandleImage
from apps.core.models import Entity

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
image_host = getattr(settings, 'IMAGE_HOST', None)


@task(base=BaseTask)
def fetch_image(images, entity_id, *args, **kwargs):
    image_list = list()
    for image_url in images:
        # print image_url
        f = urllib2.urlopen(image_url)
        # print f.read()

        image = HandleImage(f)
        # print image.image_data
        # image.name
        image_name = image_path + image.name
        image_name = image_host + default_storage.save(image_name, ContentFile(image.image_data))
        image_list.append(image_name)

    try:
        entity = Entity.objects.get(pk = entity_id)
        entity.images = image_list
        entity.save()
    except Entity.DoesNotExist, e:
        pass
    # return
# def like_task(uid, eid, **kwargs):
#
#     try:
#         obj = Entity_Like.objects.create(
#             user_id = uid,
#             entity_id = eid,
#         )
#         return obj
#     except Exception:
#         pass
#     # return status


__author__ = 'edison'

