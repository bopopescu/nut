from celery.task import task
from apps.core.tasks import BaseTask
from apps.core.models import Note_Poke

from django.utils.log import getLogger

log = getLogger('django')


@task(base=BaseTask)
def post_note_task(uid, nid):
    try:
        Note_Poke.objects.get(user_id=uid, note_id=nid)
    except Note_Poke.DoesNotExist:
        np =  Note_Poke(
            user_id=uid,
            note_id=nid,
        )
        np.save()
    log.info("poke ok ok")
    # pass

@task(base=BaseTask)
def depoke_note_task(uid, nid):
    try:
        np = Note_Poke.objects.get(user_id=uid, note_id=nid)
        np.delete()
    except Note_Poke.DoesNotExist, e:
        log.info("INFO: %s" % e.message)
    log.info("depoke ok ok")

__author__ = 'edison'
