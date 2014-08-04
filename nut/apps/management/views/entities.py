from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import Entity


def list(request, template = 'management/entities/list.html'):

    page = request.GET.get('page', 1)
    entity_list  = Entity.objects.all()

    paginator = Paginator(entity_list, 20)

    try:
        entities = paginator.page(page)
    except InvalidPage:
        entities = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(template,
                            {
                                'entities': entities,
                            },
                            context_instance = RequestContext(request))


def detail(request, entity_id,  template='management/entities/detail.html'):

    return render_to_response(template,
                        {},
                        context_instance = RequestContext(request))


__author__ = 'edison7500'
