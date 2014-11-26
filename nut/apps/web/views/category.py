from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.template import RequestContext

from apps.core.models import Category


@require_GET
def list(request, template='web/category/list.html'):

    _categories = Category.objects.filter(status=True)

    return render_to_response(
        template,
        {
            'categories': _categories,
        },
        context_instance = RequestContext(request),
    )


@require_GET
def detail(request, cid, template='web/category/detail.html'):


    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request),
    )

__author__ = 'edison7500'
