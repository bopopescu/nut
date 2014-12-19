from celery.utils.log import get_task_logger
from celery import Task, task

logger = get_task_logger(__name__)

class DebugTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        logger.info('TASK STARTING: %s[%s]' % (self.name, self.request.id))
        return self.run(*args, **kwargs)



__author__ = 'edison'
