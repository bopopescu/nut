from celery.task import task
from apps.core.tasks import BaseTask
from apps.core.models import Selection_Entity

from datetime import datetime



@task(base=BaseTask)
def set_publish_time(*args, **kwargs):

    _interval_time = kwargs.pop('interval_time', 5)
    _start_time = kwargs.pop('start_time', datetime.now())

    return


__author__ = 'edison7500'
