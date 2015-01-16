from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.core.models import Selection_Entity



def list(request, template='management/selection/list.html'):



    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request)
    )


__author__ = 'edison7500'
