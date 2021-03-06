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

from apps.core.tasks.account import fetch_avatar, update_token
from apps.core.tasks.entity import fetch_image, like_task, unlike_task, record_entity_view_task
from apps.core.tasks.selection import set_publish_time
from apps.core.tasks.note import post_note_task, depoke_note_task
from apps.core.tasks.usite import usite_published
from apps.core.tasks.recorder import record_search
from apps.core.tasks.edm import add_user_to_list
from apps.core.tasks.edm import send_activation_mail
from apps.core.tasks.edm import send_forget_password_mail
from apps.core.tasks.article import dig_task, undig_task


__author__ = 'edison'
