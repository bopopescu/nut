from celery.task import task
from apps.core.tasks import BaseTask, DebugTask

import requests
from apps.core.models import Entity, Entity_Like

record_url = 'http://127.0.0.1:7000/click_record/'

@task(base=BaseTask)
def click_record(user_id, entity_id, referer):
    requests.get(record_url, params={'user_id': user_id, 'entity_id': entity_id, 'referer': referer})
    pass



