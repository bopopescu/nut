from celery.utils.log import get_task_logger
from celery import Task

logger = get_task_logger(__name__)

class DebugTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        logger.info('TASK STARTING: %s[%s]' % (self.name, self.request.id))
        return self.run(*args, **kwargs)


class BaseTask(Task):
    abstract = True
    compression = 'gzip'
    send_error_emails = True
    default_retry_delay = 20



# from apps.core.tasks.entity import like_task

__author__ = 'edison'
