from django.shortcuts import render_to_response
from apps.core.models import Entity


def list(request, template = 'management/entities/list.html'):


    entity_list = Entity.objects.all()

    return render_to_response(template,
                              )

__author__ = 'edison7500'
