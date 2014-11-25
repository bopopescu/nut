from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.core.models import Entity



def entity_detail(request, entity_hash, templates='web/entity/detail.html'):
    _entity_hash = entity_hash

    _entity = Entity.objects.get(entity_hash = _entity_hash)


    return render_to_response(
        templates,
        {
            'entity': _entity,
        },
        context_instance = RequestContext(request),
    )




__author__ = 'edison'
