from celery.task import task
from apps.core.tasks import BaseTask, DebugTask

import requests
import settings

click_record_url = getattr(settings, 'CLICK_RECORD_URL')

@task(base=BaseTask)
def click_record(user_id, entity_id, referer):
    requests.get(click_record_url, params={'user_id': user_id, 'entity_id': entity_id, 'referer': referer})
    pass



