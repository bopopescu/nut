from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.core.models import Tag, Entity_Tag

from django.utils.log import getLogger

log = getLogger('django')


def detail(request, hash, template="web/tags/detail.html"):
    try:
        tag = Tag.objects.get(tag_hash = hash)
    except Tag.DoesNotExist:
        raise Http404

    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request),
    )

__author__ = 'edison'
