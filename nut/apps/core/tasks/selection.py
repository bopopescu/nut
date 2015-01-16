from celery.task import task
from apps.core.tasks import BaseTask
from apps.core.models import Selection_Entity

from datetime import datetime, timedelta

from django.utils.log import getLogger

log = getLogger('django')


@task(base=BaseTask)
def set_publish_time(*args, **kwargs):

    _publish_number = kwargs.pop('publish_number', 1)
    _interval_time = kwargs.pop('interval_time', 600)
    _start_time = kwargs.pop('start_time', datetime.now())


    pendings = Selection_Entity.objects.pending()

    publish_lastest = Selection_Entity.objects.published().first()

    while _publish_number:
        i = 0
        s = pendings[i]
        log.info(publish_lastest)
        if s.entity.category_id == publish_lastest.entity.category_id or s.entity.top_note.user_id == publish_lastest.entity.top_note.user_id:
            i += 1
            continue
        else:
            s.is_published = True
            s.pub_time = _start_time
            s.save()

        _start_time += timedelta(seconds=_interval_time)
        _publish_number -= 1


__author__ = 'edison7500'
