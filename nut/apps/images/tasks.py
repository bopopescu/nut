from celery.task import task
from apps.core.tasks import DebugTask, BaseTask
from apps.core.utils.image import HandleImage
from django.core.files.storage import default_storage


@task(base=BaseTask)
def resize(image_name, size=None, **kwargs):

    f = default_storage.open(image_name)

    try:
        if size is not None:
            image = HandleImage(f)
            _size = float(size)
            image.resize(_size, _size)
            image_data = image.image_data
        else:
            image_data = f.read()
    except AttributeError:
        return None

    return image_data

__author__ = 'edison'
