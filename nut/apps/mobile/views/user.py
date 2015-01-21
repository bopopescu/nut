from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Entity_Tag, GKUser, Entity_Like, Note
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger

from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key

from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger
from datetime import datetime
import time


log = getLogger('django')


@csrf_exempt
@check_sign
def update(request):


    if request.method == "POST":
        log.info(request.POST)
        log.info(request.FILES)
        return

    return ErrorJsonResponse(status=400)


@check_sign
def detail(request, user_id):
    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        raise ErrorJsonResponse(status=404)

    _last_like = Entity_Like.objects.filter(user=_user).last()
    _last_note = Note.objects.filter(user=_user).last()

    res = dict()
    res['user'] = _user.v3_toDict()
    if _last_like:
        res['last_like'] = _last_like.entity.v3_toDict()
    if _last_note:
        res['last_note'] = _last_note.v3_toDict()

    return SuccessJsonResponse(res)


@check_sign
def tag_list(request, user_id):

    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    # _key = request.GET.get('session')
    #
    # try:
    #     _session = Session_Key.objects.get(session_key = _key)
    # except Session_Key.DoesNotExist:
    #     pass

    res = {}
    res['user'] = _user.v3_toDict()
    res['tags'] = Entity_Tag.objects.user_tags(user=_user.pk)
    return SuccessJsonResponse(res)


@check_sign
def tag_detail(request, user_id, tag):
    _key = request.GET.get('session')




    try:
        user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    tags = Entity_Tag.objects.filter(user_id=user_id, tag__tag=tag)


    try:
        _session = Session_Key.objects.get(session_key = _key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(tags.values_list('entity_id', flat=True)))
    except Session_Key.DoesNotExist:
        el = None

    res = dict()
    res['user'] = user.v3_toDict()
    res['entity_list'] = []
    for row in tags:
        entity = row.entity
        res['entity_list'].append(entity.v3_toDict(user_like_list=el))
        # log.info(entity)

    log.info(res)

    return SuccessJsonResponse(res)


@check_sign
def entity_like(request, user_id):

    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    _timestamp = request.GET.get('timestamp', datetime.now())
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))

    _offset = _offset / _count + 1

    res = {}
    res['timestamp'] = time.mktime(_timestamp.timetuple())
    res['entity_list'] = []

    entity_list = Entity_Like.objects.filter(user=_user, created_time__lte=datetime.now())

    paginator = ExtentPaginator(entity_list, _count)

    try:
        entities = paginator.page(_offset)
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)

    for like in entities.object_list:
        res['entity_list'].append(
            like.entity.v3_toDict()
        )

    return SuccessJsonResponse(res)

@check_sign
def entity_note(request, user_id):
    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))

    _offset = _offset / _count + 1

    _timestamp = request.GET.get('timestamp', datetime.now())
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))



    note_list = Note.objects.filter(user=_user, post_time__lte=_timestamp)

    paginator = ExtentPaginator(note_list, _count)
    try:
        notes = paginator.page(_offset)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)


    res = []

    for note in notes.object_list:
        log.info(note)
        res.append({
            'note':note.v3_toDict(),
            'entity':note.entity.v3_toDict(),
        })

    return SuccessJsonResponse(res)

__author__ = 'edison7500'
