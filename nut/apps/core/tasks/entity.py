from celery.task import task
from apps.core.tasks import BaseTask
from apps.core.models import Entity_Like

# @task(base=BaseTask)
# def like_task(uid, eid, **kwargs):
#
#     try:
#         obj = Entity_Like.objects.create(
#             user_id = uid,
#             entity_id = eid,
#         )
#         return obj
#     except Exception:
#         pass
#     # return status


__author__ = 'edison'

