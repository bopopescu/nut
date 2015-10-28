from celery.task import task
from apps.core.tasks import BaseTask, DebugTask

from apps.core.models import Article, Article_Dig

@task(base=BaseTask)
def dig_task(uid, aid, **kwargs):
    try:
        Article_Dig.objects.get(user_id=uid, article_id=aid)
    except Article_Dig.DoesNotExist as e:
        obj = Article_Dig.objects.create(
            user_id = uid,
            article_id = aid,
        )
        obj.article.incr_dig()
        obj.user.incr_dig()
        return obj


@task(base=BaseTask)
def undig_task(uid,aid, **kwargs):
    try:
        obj = Article_Dig.objects.get(user_id=uid, article_id=aid)
        obj.delete()
        obj.article.decr_dig()
        obj.user.decr_dig()
        return True
    except Article_Dig.DoesNotExist as e :
        return False

