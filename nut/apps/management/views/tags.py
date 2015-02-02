from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext_lazy as _

from apps.core.models import Tag, Entity_Tag
from apps.core.forms.tags import EditTagForms
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


def edit(request, tag_id, template='management/tags/edit.html'):

    try:
        _tag = Tag.objects.get(pk = tag_id)
    except Tag.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = EditTagForms(_tag, request.POST)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = EditTagForms(_tag, initial={
            'title':_tag.tag,
        })


    return render_to_response(
        template,
        {
            'forms': _forms,
            'button': _('update'),
        },
        context_instance = RequestContext(request)
    )


def entities(request, tag_id, templates="management/tags/entities.html"):


    return render_to_response(
        templates,
        {

        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
