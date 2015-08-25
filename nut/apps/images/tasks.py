from celery.task import task
from apps.core.tasks import DebugTask, BaseTask
from apps.core.utils.image import HandleImage
from django.core.files.storage import default_storage
from celery.utils.log import get_task_logger
import requests
from StringIO import StringIO
from django.conf import settings

logger = get_task_logger(__name__)

intranet_image_server = getattr(settings, 'INTRANET_IMAGE_SERVER', 'http://10.0.2.50/')

@task(base=BaseTask)
def resize(image_name, size=None, **kwargs):
    # print image_name
    url = intranet_image_server + image_name
    r = requests.get(url)
    # f = default_storage.open(image_name)
    f = StringIO(r.content)

    try:
        if size is not None:
            image = HandleImage(f)
            _size = float(size)
            # logger.info(image.content_type)
            # print image
            image.resize(_size, _size)
            image_data = image.image_data
        else:
            image_data = f.read()
    except AttributeError:
        logger.error("Error: %s" % image_name)
        return None

    return image_data

__author__ = 'edison'
