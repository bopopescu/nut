from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import Show_Banner, Entity


def dashboard(request, template='management/dashboard.html'):

    page = request.GET.get('page', 1)

    show_banners = Show_Banner.objects.all()

    selection_entity_list = Entity.objects.filter(status = Entity.selection)

    paginator = Paginator(selection_entity_list, 30)

    try:
        selection_entities = paginator.page(page)
    except InvalidPage:
        selection_entities = paginator.page(1)
    except EmptyPage:
        raise Http404


    return render_to_response(template,
                                {
                                    'show_banners': show_banners,
                                    'selection_entities': selection_entities,
                                },
                                context_instance = RequestContext(request))


__author__ = 'edison7500'
