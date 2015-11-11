from celery.task import task
from apps.core.tasks import BaseTask, DebugTask

import urllib2
import requests
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
from apps.core.utils.image import HandleImage
from apps.core.models import Entity, Entity_Like

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
image_host = getattr(settings, 'IMAGE_HOST', None)


@task(base=BaseTask)
def fetch_image(images, entity_id, *args, **kwargs):
    image_list = list()
    for image_url in images:
        if 'http' not in image_url:
            image_url = 'http:' + image_url
        # f = urllib2.urlopen(image_url)
        if image_host in image_url:
            image_list.append(image_url)
            continue

        r = requests.get(image_url, stream=True)
        image = HandleImage(r.raw)
        image_name = image.save()
        image_list.append("%s%s" % (image_host, image_name))
    try:
        entity = Entity.objects.get(pk = entity_id)
        entity.images = image_list
        entity.save()
    except Entity.DoesNotExist, e:
        pass
    # return



@task(base=BaseTask)
def like_task(uid, eid, **kwargs):

    try:
        Entity_Like.objects.get(user_id=uid, entity_id=eid)
    except Entity_Like.DoesNotExist as  e:
        obj = Entity_Like.objects.create(
            user_id = uid,
            entity_id = eid,
        )
        obj.entity.innr_like()
        obj.user.incr_like()
        return obj
    # return status


@task(base=BaseTask)
def unlike_task(uid, eid, **kwargs):
    try:
        obj = Entity_Like.objects.get(user_id=uid, entity_id=eid)
        obj.delete()
        obj.entity.decr_like()
        obj.user.decr_like()
        return True
    except Entity_Like.DoesNotExist:
        return False

__author__ = 'edison'

