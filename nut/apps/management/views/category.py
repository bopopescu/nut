from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.core.models import Category
from apps.core.forms.category import EditCategoryForm
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage

def list(request, template='management/category/list.html'):
    #
    # c = request.GET.get('c', '1')
    page = request.GET.get('page', 1)

    categories = Category.objects.all()

    # category = Category.objects.get(pk = category_id)
    # sub_category_list = category.sub_categories.all()

    paginator = ExtentPaginator(categories, 30)

    # try:
    #     sub_categories = paginator.page(page)
    # except PageNotAnInteger:
    #     sub_categories = paginator.page(1)
    # except EmptyPage:
    #      raise Http404
    try:
        category_list = paginator.page(page)
    except PageNotAnInteger:
        category_list = paginator.page(1)
    except EmptyPage:
        raise Http404


    return render_to_response(
        template,
        {
            # 'current_category_id': int(category_id),
            'category_list': category_list,
            # 'sub_categories': sub_categories,
        },
        context_instance = RequestContext(request)
    )


def edit(request, cid, template="management/category/edit.html"):

    try:
        category = Category.objects.get(pk = cid)
    except Category.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = EditCategoryForm(category=category, data=request.POST)
        if _forms.is_valid():
            _forms.save()
            return 
    else:
        _forms = EditCategoryForm(
            category=category,
            initial={
                'title': category.title,
                'status': category.status,
            }
        )

    return render_to_response(
        template,
        {
            'forms':_forms,
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
