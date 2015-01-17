from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from datetime import datetime
import time

from apps.core.models import Entity
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from django.utils.log import getLogger
import random


log = getLogger('django')


@check_sign
def list(request):

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

    entity_list = Entity.objects.new()

    paginator = ExtentPaginator(entity_list, _count)

    try:
        entities = paginator.page(_offset)
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)
    # res = list
    res = []
    for row in entities.object_list:
        res.append(
            row.v3_toDict()
        )

    return SuccessJsonResponse(res)


@check_sign
def detail(request, entity_id):

    res = dict()
    try:
        entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        return ErrorJsonResponse(status=404)

    res['entity'] = entity.v3_toDict()
    res['note_list'] = []

    # notes = entity.notes.all()
    # log.info(notes)
    for note in entity.notes.all():
        res['note_list'].append(
            note.v3_toDict()
        )

    return SuccessJsonResponse(res)


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
