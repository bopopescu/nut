from django.views.decorators.http import require_GET

from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Category, Sub_Category, Entity, Note
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.mobile.lib.sign import check_sign

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

    res = dict()

    res['entity_count'] = Entity.objects.filter(category_id=category_id, status__gte=0).count()
    res['entity_note_count'] = Note.objects.filter(entity__category_id=category_id).count()
    res['like_count'] = 0

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
        # log.info(row.toDict())

        r = row.toDict()
        r.pop('images', None)
        r.pop('id', None)
        res.append(
            r
        )
    return SuccessJsonResponse(res)

__author__ = 'edison'
