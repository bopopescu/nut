from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from apps.core.models import Category, Sub_Category, Entity
from apps.core.forms.category import CreateCategoryForm, EditCategoryForm, CreateSubCategoryForm, EditSubCategoryForm
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.utils.http import JSONResponse
# import json

from django.utils.log import getLogger

log = getLogger('django')


@login_required
def list(request, template='management/category/list.html'):
    #
    # c = request.GET.get('c', '1')
    if request.is_ajax():

        res = {}
        # res[''] = {}
        categories = Category.objects.all()

        for c in categories:
            res[c.id] = []
            for s in c.sub_categories.all().order_by('alias'):
                res[c.id].append(
                    {
                        'category_id': s.id,
                        'category_title': s.title,
                    }
                )
                # log.info(s)
        return JSONResponse(res)
        # return HttpResponse(json.dumps(res))

    page = request.GET.get('page', 1)

    categories = Category.objects.all().order_by('-status')

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


@login_required
def sub_category_list(request, cid, template="management/category/sub_category_list.html"):

    _page = request.GET.get('page', 1)
    try:
        category = Category.objects.get(pk = cid)
    except Category.DoesNotExist:
        raise Http404

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
            'category': category,
            'category_list': category_list,
        },
        context_instance = RequestContext(request)
    )


def sub_category_create(request, cid, template="management/category/sub_category_create.html"):
    try:
        category = Category.objects.get(pk = cid)
    except Category.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = CreateSubCategoryForm(request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = CreateSubCategoryForm(initial={
            'category':category.pk,
        })

    return render_to_response(
        template,
        {
            'forms': _forms,
            'button': _('add'),
        },
        context_instance = RequestContext(request)
    )


def sub_category_edit(request, scid, template="management/category/sub_category_edit.html"):

    _update = False

    try:
        sub_category = Sub_Category.objects.get(pk = scid)
    except Sub_Category.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        _forms = EditSubCategoryForm(sub_category=sub_category, data=request.POST, files=request.FILES)
        if _forms.is_valid():
            _forms.save()
            _update = True
            # return HttpResponseRedirect()
    else:
        _forms = EditSubCategoryForm(
            sub_category=sub_category,
            initial={
                'category':sub_category.group_id,
                'title':sub_category.title,
                'status': int(sub_category.status),
            }
        )

    return render_to_response(
        template,
        {
            'sub_category':sub_category,
            'forms':_forms,
            'update': _update,
            'button':_('update'),
        },
        context_instance = RequestContext(request)
    )


def create(request, template="management/category/create.html"):

    if request.method == "POST":
        _forms = CreateCategoryForm(data=request.POST, files=request.FILES)
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
        # print request.FILES
        _forms = EditCategoryForm(category=category, data=request.POST, files=request.FILES)
        if _forms.is_valid():
            category = _forms.save()
            return HttpResponseRedirect(reverse('management_category_list'))
    else:
        _forms = EditCategoryForm(
            category=category,
            initial={
                'title': category.title,
                'status': int(category.status),
            }
        )

    return render_to_response(
        template,
        {
            'category': category,
            'forms':_forms,
            'button': _('update'),
        },
        context_instance = RequestContext(request)
    )


def category_entity_list(request, cid, templates = 'management/category/entity/category_entity_list.html'):

    _category = get_object_or_404(Category, pk=cid)

    page = request.GET.get('page', 1)
    status = request.GET.get('status', None)

    inner_qs = Sub_Category.objects.filter(group_id = cid)

    if status is None:
        entities = Entity.objects.filter(category__in=inner_qs)
    else:
        entities = Entity.objects.filter(category__in=inner_qs, status = int(status))

    paginator = ExtentPaginator(entities, 30)
    try:
        _entity_list = paginator.page(page)
    except PageNotAnInteger:
        _entity_list = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        templates,
        {
            'entities': _entity_list,
            'category':_category,
            'status': status,
        },
        context_instance = RequestContext(request)
    )


def sub_category_entity_list(request, scid, templates='management/category/entity/sub_category_entity_list.html'):
    page = request.GET.get('page', 1)
    status = request.GET.get('status', None)

    _sub_category = get_object_or_404(Sub_Category, pk=scid)

    if status is None:
        entities = Entity.objects.filter(category=_sub_category)
    else:
        entities = Entity.objects.filter(category=_sub_category, status=int(status))

    paginator = ExtentPaginator(entities, 30)
    try:
        _entity_list = paginator.page(page)
    except PageNotAnInteger:
        _entity_list = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        templates,
        {
            'entities': _entity_list,
            'category':_sub_category,
            'status': status,
        },
        context_instance = RequestContext(request)
    )


__author__ = 'edison'
