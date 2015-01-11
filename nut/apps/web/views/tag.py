from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.core.models import Tag, Entity_Tag, Entity
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from django.utils.log import getLogger

log = getLogger('django')


def detail(request, hash, template="web/tags/detail.html"):
    try:
        _tag = Tag.objects.get(tag_hash = hash)
    except Tag.DoesNotExist:
        raise Http404

    _page = request.GET.get('page', 1)

    # inner_qs = Entity_Tag.objects.filter(tag=_tag)
    # log.info(e)
    inner_qs = Entity_Tag.objects.filter(tag=_tag).values_list('entity_id', flat=True)
    _entity_list = Entity.objects.filter(id__in=inner_qs, status=Entity.selection)
    # log.info(entities)
    paginator = ExtentPaginator(_entity_list, 24)

    try:
        _entities = paginator.page(_page)
    except PageNotAnInteger:
        _entities = paginator.page(1)
    except EmptyPage:
        raise Http404


    return render_to_response(
        template,
        {
            'tag': _tag,
            'entities':_entities,
        },
        context_instance = RequestContext(request),
    )

__author__ = 'edison'
