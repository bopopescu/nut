from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Entity, Entity_Like, Note_Poke
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
# from apps.core.models import Entity_Like
from apps.core.tasks import like_task, unlike_task
from apps.mobile.models import Session_Key
from apps.mobile.forms.search import EntitySearchForm
from apps.report.models import Report
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
        entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        return ErrorJsonResponse(status=404)

    try:
        _session = Session_Key.objects.get(session_key=_key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=[entity_id])
        np = Note_Poke.objects.user_poke_list(user=_session.user,  note_list=list(entity.notes.values_list('id', flat=True)))
        # np = Note_Poke.objects.filter(user=_session.user, note_id__in=list(entity.notes.values_list('id', flat=True))).values_list('note_id', flat=True)
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None
        np = None

    # log.info(np)
    # log.info(el)
    res = dict()

    res['entity'] = entity.v3_toDict(user_like_list=el)
    res['note_list'] = []
    for note in entity.notes.filter(status__gte=0):
        res['note_list'].append(
            note.v3_toDict(user_note_pokes=np)
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



@require_GET
@check_sign
def search(request):

    _type = request.GET.get('type', None)

    # _query_string = request.GET.get('q')
    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))

    _offset = _offset / _count + 1

    _key = request.GET.get('session', None)


    try:
        _session = Session_Key.objects.get(session_key=_key)
        visitor = _session.user
    except Session_Key.DoesNotExist:
        visitor = None


    _forms = EntitySearchForm(request.GET)

    if _forms.is_valid():
        results = _forms.search()
        log.info(results.count())
        res = {
            'stat' : {
                'all_count' : results.count(),
                'like_count' : 0,
            },
            'entity_list' : []
        }



        el = None
        if visitor:
            _entity_id_list = map(lambda x : int(x._sphinx['id']), results)
            el = Entity_Like.objects.user_like_list(user = visitor, entity_list=_entity_id_list)
            log.info(el)

        if _type == 'like':
            like_entity_list = Entity.objects.filter(pk__in=el)
            paginator = ExtentPaginator(like_entity_list, _count)
            try:
                entities = paginator.page(_offset)
            except PageNotAnInteger:
                entities = paginator.page(1)
            except EmptyPage:
                return ErrorJsonResponse(status=404)
            for entity in entities:
                res['entity_list'].append(
                    entity.v3_toDict(user_like_list=el)
                )
                res['stat']['like_count'] = len(el)
            return SuccessJsonResponse(res)

        paginator = ExtentPaginator(results, _count)
        try:
            entities = paginator.page(_offset)
        except PageNotAnInteger:
            entities = paginator.page(1)
        except EmptyPage:
            return ErrorJsonResponse(status=404)
        for entity in entities:
            # log.info(entity)
            res['entity_list'].append(
                entity.v3_toDict(user_like_list=el)
            )
        res['stat']['like_count'] = len(el)
        return SuccessJsonResponse(res)
    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def report(request, entity_id):
    _key = request.POST.get('session')
    _comment = request.POST.get('comment', '')
    try:
        _session = Session_Key.objects.get(session_key=_key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=400)

    try:
        entity = Entity.objects.get(pk = entity_id)
    except Entity.DoesNotExist:
        return ErrorJsonResponse(status=404)

    r = Report(reporter=_session.user, comment=_comment, content_object=entity)
    r.save()
    return SuccessJsonResponse({ "status" : 1 })

__author__ = 'edison'
