from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.core.models import Tag


def list(request, template='management/tags/list.html'):


    return render_to_response(
            template,
            {

            },
            context_instance = RequestContext(request)
            )

__author__ = 'edison'
