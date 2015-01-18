from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Entity_Tag, GKUser, Entity_Like, Note
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger

from django.utils.log import getLogger
from datetime import datetime
import time


log = getLogger('django')

@check_sign
def detail(request, user_id):
    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        raise ErrorJsonResponse(status=404)

    _last_like = Entity_Like.objects.filter(user=_user).last()
    _last_note = Note.objects.filter(user=_user).last()
    # log.info(last_like)
    # log.info(last_note)


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

    res = {}
    res['user'] = _user.v3_toDict()
    res['tags'] = Entity_Tag.objects.user_tags(user=_user.pk)
    return SuccessJsonResponse(res)

@check_sign
def tag_detail(request, user_id, tag):

    try:
        user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    tags = Entity_Tag.objects.filter(user_id=user_id, tag__tag=tag)

    # log.info(tags)
    # log.in
    res = dict()
    res['user'] = user.v3_toDict()
    res['entity_list'] = []
    for row in tags:
        entity = row.entity
        res['entity_list'].append(entity.v3_toDict())
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
