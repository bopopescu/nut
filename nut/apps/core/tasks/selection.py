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
    _st = kwargs.pop('start_time')

    _start_time = datetime.strptime(_st, "%Y-%m-%d %H:%M:%S")

    pendings = Selection_Entity.objects.pending()
    pendings = list(pendings)
    publish_lastest = Selection_Entity.objects.published().first()

    i = 0
    while _publish_number:

        try:
            s = pendings[i]
        except IndexError:
            break
        # log.info(publish_lastest)
        if publish_lastest is None:
            s.is_published = True
            log.info(_start_time)
            s.pub_time = _start_time
            s.save()
            publish_lastest = s
            pendings.pop(i)
            # continue
        # log.info(publish_lastest)

        if s.entity.category.group_id == publish_lastest.entity.category.group_id:
            i += 1
            log.info("category %s %s", (s.entity.category_id, publish_lastest.entity.category_id))
            continue
        else:
            s.is_published = True
            log.info(_start_time)
            s.pub_time = _start_time
            s.save()
            publish_lastest = s
            pendings.pop(i)

        i = 0
        _start_time += timedelta(seconds=_interval_time)
        _publish_number -= 1


__author__ = 'edison7500'
