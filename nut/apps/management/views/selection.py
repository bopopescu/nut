from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from apps.core.models import Selection_Entity, Entity
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage

from django.utils.log import getLogger

log = getLogger('django')


def selection_list(request, template='management/selection/list.html'):

    _page = request.GET.get('page', 1)

    s = Selection_Entity.objects.all().values_list('entity_id', flat=True)
    # log.info(s.query)
    paginator = ExtentPaginator(s, 30)

    try:
        selections = paginator.page(_page)
    except PageNotAnInteger:
        selections = paginator.page(1)
    except EmptyPage:
        raise Http404

    # log.info(selections.object_list)
    # innqs = selections.object_list
    _entities = Entity.objects.filter(id__in=list(selections.object_list))

    return render_to_response(
        template,
        {
            'selections': selections,
            'entities': _entities,
        },
        context_instance = RequestContext(request)
    )


__author__ = 'edison7500'
