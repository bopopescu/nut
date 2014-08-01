from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.core.models import Entity


def list(request, template = 'management/entities/list.html'):


    entities  = Entity.objects.all()

    return render_to_response(template,
                            {

                            },
                            context_instance = RequestContext(request))


def detail(request, entity_id,  template='management/entities/detail.html'):

    return render_to_response(template,
                        {},
                        context_instance = RequestContext(request))


__author__ = 'edison7500'
