from celery.task import task
from celery.utils.log import get_task_logger

from apps.core.tasks import BaseTask, DebugTask

import requests
from apps.core.utils.image import HandleImage
from apps.core.models import Entity, Entity_Like, EntityViewRecord

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
image_host = getattr(settings, 'IMAGE_HOST', None)


logger = get_task_logger(__name__)


@task(base=BaseTask)
def fetch_image(images, entity_id, *args, **kwargs):
    image_list = list()
    for image_url in images:
        if 'http' not in image_url:
            image_url = 'http:' + image_url
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


@task(base=BaseTask)
def like_task(uid, eid, **kwargs):

    try:
        Entity_Like.objects.get(user_id=uid, entity_id=eid)
    except Entity_Like.DoesNotExist as e:
        obj = Entity_Like.objects.create(
            user_id = uid,
            entity_id = eid,
        )
        obj.entity.innr_like()
        obj.user.incr_like()
        return obj


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


@task(base=DebugTask)
def record_entity_view_task(entity_id, user_id, device_uuid, **kwargs):
    try:
        EntityViewRecord.objects.create(entity_id=entity_id, user_id=user_id, device_uuid=device_uuid)
    except Exception as e:
        logger.error(e)
