from django.views.decorators.csrf import csrf_exempt
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
# from apps.core.models import Entity_Like
from apps.core.tasks import like_task, unlike_task
from apps.mobile.models import Session_Key

from datetime import datetime
import time
import random


from django.utils.log import getLogger
log = getLogger('django')


@check_sign
def entity_list(request):

    _timestamp = request.GET.get('timestamp', None)
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))

    _sort_by = request.GET.get('sort', 'novus_time')
    _reverse = request.GET.get('reverse', '0')
    if _reverse == '0':
        _reverse = False
    else:
        _reverse = True

    _offset = int(request.GET.get('offset', '0'))
    _offset = _offset / 30 + 1
    _count = int(request.GET.get('count', '30'))


    _key = request.GET.get('session', None)
    # log.info("session "_key)


    entity_list = Entity.objects.new()

    paginator = ExtentPaginator(entity_list, _count)

    try:
        entities = paginator.page(_offset)
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)
    # res = list

    try:
        _session = Session_Key.objects.get(session_key=_key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(entities.object_list))
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None

    res = []
    for row in entities.object_list:
        res.append(
            row.v3_toDict(user_like_list=el)
        )

    return SuccessJsonResponse(res)


@check_sign
def detail(request, entity_id):

    _key = request.GET.get('session', None)
    # log.info("session "_key)
    try:
        _session = Session_Key.objects.get(session_key=_key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=[entity_id])
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None

    res = dict()
    try:
        entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        return ErrorJsonResponse(status=404)


    log.info(el)
    res['entity'] = entity.v3_toDict(user_like_list=el)
    res['note_list'] = []
    for note in entity.notes.filter(status__gte=0):
        res['note_list'].append(
            note.v3_toDict()
        )

    res['like_user_list'] = []
    for liker in entity.likes.all()[0:10]:
        res['like_user_list'].append(
            liker.user.v3_toDict()
        )

    return SuccessJsonResponse(res)


@csrf_exempt
@check_sign
def like_action(request, entity_id, target_status):
    if request.method == "POST":
        _key = request.POST.get('session', None)
        try:
            _session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)
        res = {
            'entity_id': entity_id,
        }

        if target_status == "1":
            like_task.delay(uid=_session.user_id, eid=entity_id)
            res['like_already'] = 1
        else:
            unlike_task.delay(uid=_session.user_id, eid=entity_id)
            res['like_already'] = 0
        return SuccessJsonResponse(res)

    return ErrorJsonResponse(status=400)

@check_sign
def guess(request):

    res = []

    _category_id = request.GET.get('cid', None)
    _count = int(request.GET.get('count', '5'))

    entities = Entity.objects.guess(category_id=_category_id, count=_count)

    for entity in entities:
        res.append(entity.v3_toDict())

    return SuccessJsonResponse(res)

__author__ = 'edison'
