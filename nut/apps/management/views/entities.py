from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import Entity
from apps.core.forms.entity import EntityFrom

def list(request, template = 'management/entities/list.html'):

    page = request.GET.get('page', 1)
    entity_list  = Entity.objects.all()

    paginator = Paginator(entity_list, 30)

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


def edit(request, entity_id,  template='management/entities/edit.html'):

    if request.method == "POST":

        pass

    try:
        entity = Entity.objects.get(pk = entity_id)
    except Entity.DoesNotExist:
        raise Http404

    _forms = EntityFrom(
        initial={
            'id':entity.pk,
        }
    )
    return render_to_response(template,
                        {
                            'entity': entity,
                            'forms':_forms,
                        },
                        context_instance = RequestContext(request))


__author__ = 'edison7500'
