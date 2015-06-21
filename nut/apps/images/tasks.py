from celery.task import task
from apps.core.tasks import DebugTask, BaseTask
from apps.core.utils.image import HandleImage
from django.core.files.storage import default_storage
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@task(base=BaseTask)
def resize(image_name, size=None, **kwargs):
    # logger.info(image_name)
    f = default_storage.open(image_name)

    try:
        if size is not None:
            image = HandleImage(f)
            _size = float(size)
            # logger.info(image.image_data)
            image.resize(_size, _size)
            image_data = image.image_data
        else:
            image_data = f.read()
    except AttributeError:
        logger.error("Error: %s" % image_name)
        return None

    return image_data

__author__ = 'edison'
