from django.views.decorators.http import require_GET

from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Category, Sub_Category, Entity, Entity_Like,  Note
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key

from django.utils.log import getLogger

log = getLogger('django')



@require_GET
@check_sign
def list(request):

    res = Category.objects.toDict()
    # res = []
    return SuccessJsonResponse(res)


@require_GET
@check_sign
def stat(request, category_id):

    _key = request.GET.get('session')
    res = dict()
    entities = Entity.objects.filter(category_id=category_id, status__gte=0)
    res['entity_count'] = entities.count()
    res['entity_note_count'] = Note.objects.filter(entity__category_id=category_id).count()

    try:
        _session = Session_Key.objects.get(session_key = _key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=entities.values_list('id', flat=True))
        # Entity.objects.filter()
        res['like_count'] = el.count()
    except Session_Key.DoesNotExist:
        res['like_count'] = 0





    # res['like_count'] = 0

    return SuccessJsonResponse(res)


@require_GET
@check_sign
def entity(request, category_id):

    _offset = int(request.GET.get('offset', '0'))
    _offset = _offset / 30 + 1
    _count = int(request.GET.get('count', '30'))

    # entity_list = Entity.objects.filter(category_id=category_id, status__gte=0)
    entity_list = Entity.objects.new_or_selection(category_id=category_id)
    paginator = ExtentPaginator(entity_list, _count)

    try:
        entities = paginator.page(_offset)
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)

    res = []
    for row in entities.object_list:

        r = row.toDict()
        r.pop('images', None)
        r.pop('id', None)
        res.append(
            r
        )
    return SuccessJsonResponse(res)


@require_GET
@check_sign
def entity_note(request, category_id):

    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))

    _offset = _offset / _count + 1


    res = []

    note_list = Note.objects.filter(entity__category_id=category_id)

    paginator = ExtentPaginator(note_list, _count)

    try:
        notes = paginator.page(_offset)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)

    for n in notes.object_list:
        # log.info(n)
        res.append({
            'note': n.v3_toDict(),
            'entity': n.entity.v3_toDict(),
        })



    return SuccessJsonResponse(res)

__author__ = 'edison'
