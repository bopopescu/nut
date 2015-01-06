from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Category, Sub_Category
from apps.core.forms.category import CreateCategoryForm, EditCategoryForm
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage


def list(request, template='management/category/list.html'):
    #
    # c = request.GET.get('c', '1')
    page = request.GET.get('page', 1)

    categories = Category.objects.all().order_by('-id')

    paginator = ExtentPaginator(categories, 30)
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

def sub_category_list(request, cid, template="management/category/sub_category_list.html"):

    _page = request.GET.get('page', 1)
    sub_categories = Sub_Category.objects.filter(group_id = cid)

    paginator = ExtentPaginator(sub_categories, 30)

    try:
        category_list = paginator.page(_page)
    except PageNotAnInteger:
        category_list = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'category_list': category_list,
        },
        context_instance = RequestContext(request)
    )


def create(request, template="management/category/create.html"):

    if request.method == "POST":
        _forms = CreateCategoryForm(request.POST)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = CreateCategoryForm()

    return render_to_response(
        template,
        {
            "forms":_forms,
            "button": _('add')
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
            category = _forms.save()
            return HttpResponseRedirect(reverse('management_category_list'))
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
            'button': _('update'),
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
