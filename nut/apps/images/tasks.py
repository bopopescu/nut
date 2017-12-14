from celery.task import task
from apps.core.tasks import BaseTask


@task(base=BaseTask)
def resize(image_name, size=None, **kwargs):
    # deprecated
    pass
