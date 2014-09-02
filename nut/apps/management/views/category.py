from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.core.models import Category
from apps.core.extend.paginator import ExtentPaginator, InvalidPage, EmptyPage

def list(request, template='management/category/list.html'):

    c = request.GET.get('c', '1')
    page = request.GET.get('page', 1)

    categories = Category.objects.all()

    category = Category.objects.get(pk = c)
    sub_category_list = category.sub_categories.all()

    paginator = ExtentPaginator(sub_category_list, 30)

    try:
        sub_categories = paginator.page(page)
    except InvalidPage:
        sub_categories = paginator.page(1)
    except EmptyPage:
         raise Http404

    return render_to_response(
        template,
        {
            'categories': categories,
            'sub_categories': sub_categories,
        },
        context_instance = RequestContext(request)
    )


__author__ = 'edison'
