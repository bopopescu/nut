# -*- coding: utf-8 -*-

from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import  Entity_Like
from django.http import Http404


def get_paged_list(the_list, page_num=1, item_per_page=24):
    paginator = ExtentPaginator(the_list, item_per_page)
    try:
        _entities = paginator.page(page_num)
    except PageNotAnInteger:
        _entities = paginator.page(1)
    except EmptyPage:
        raise Http404
    return _entities

# NOT ready
def get_entity_like_list(entity_list, request):
    el = []
    if request.user.is_authenticated():
        e = entity_list.object_list
        el = Entity_Like.objects.filter(entity_id__in=tuple(e), user=request.user).values_list('entity_id', flat=True)
    return el