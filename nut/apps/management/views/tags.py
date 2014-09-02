from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.core.models import Tag
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage

def list(request, template='management/tags/list.html'):

    page = request.GET.get('page', 1)
    tag_list = Tag.objects.all()

    paginator = ExtentPaginator(tag_list, 30)
    try:
        _tags = paginator.page(page)
    except InvalidPage:
        _tags = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
            template,
            {
                'tags': _tags,
            },
            context_instance = RequestContext(request)
        )


def edit(request, template='management/tags/edit.html'):


    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
