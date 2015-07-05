from celery.task import task
from apps.core.tasks import BaseTask
from apps.core.models import Entity, Buy_Link
from apps.core.utils.taobaoapi.publish_item2u import PublishItem2U, UpdateItem2U
import json
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


app_key='23198909'
app_secret='cc35120d1fb84446300eb1092fae4abe'

@task(base=BaseTask)
def usite_published(eids, **kwargs):
    assert eids is not None
    # print kwargs
    # entity_json = kwargs.pop('entityids')
    # logger.info(eids)
    obj = json.loads(eids)

    for entity_id in obj:
        entity = Entity.objects.get(pk = entity_id)
        try:
            item = Buy_Link.objects.filter(entity_id=entity.pk, origin_source='taobao.com').first()
        except IndexError, e:
            logger.error(e.message)
            continue

        p = PublishItem2U(app_key='23198909', app_secret='cc35120d1fb84446300eb1092fae4abe')

        resp = p.publish(
            item_id=item.origin_id,
            title=entity.title,
            comments = entity.top_note.note,
            category = entity.category.title,
            detailurl='http://guoku.uz.taobao.com/detail/%s/' % entity.entity_hash,
        )
        try:
            uid = resp['sp_content_item_publish_response']['value']
        except KeyError, e:
            logger.error("Error: %s" % e.message)
            continue

        u = UpdateItem2U(app_key='23198909', app_secret='cc35120d1fb84446300eb1092fae4abe')
        resp = u.update(
            id = uid,
            item_id=item.origin_id,
            title=entity.title,
            comments = entity.top_note.note,
            detailurl='http://guoku.uz.taobao.com/detail/%s/' % uid,
        )
        print resp

__author__ = 'edison'
