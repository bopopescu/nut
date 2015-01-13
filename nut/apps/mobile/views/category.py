from django.views.decorators.http import require_GET

from apps.core.utils.http import SuccessJsonResponse
from apps.core.models import Category, Sub_Category, Entity, Note
from apps.mobile.lib.sign import check_sign




@require_GET
@check_sign
def list(request):

    res = Category.objects.toDict()
    # res = []
    return SuccessJsonResponse(res)


@require_GET
@check_sign
def category_stat(request, category_id):

    res = dict()

    res['entity_count'] = Entity.objects.filter(category_id=category_id, status__gte=0).count()
    res['entity_note_count'] = Note.objects.filter(entity__category_id=category_id).count()
    res['like_count'] = 0

    return SuccessJsonResponse(res)

__author__ = 'edison'
