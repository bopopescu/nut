import requests

from hashlib import md5
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotAllowed
from django.utils.log import getLogger
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from apps.core.extend.paginator import EmptyPage
from apps.core.extend.paginator import ExtentPaginator
from apps.core.extend.paginator import PageNotAnInteger
from apps.core.forms.entity import EditEntityForm
from apps.core.forms.entity import EntityImageForm
from apps.core.forms.entity import CreateEntityForm
from apps.core.forms.entity import load_entity_info
from apps.core.forms.entity import BuyLinkForm
from apps.core.forms.entity import EditBuyLinkForm
from apps.core.mixins.views import FilterMixin
from apps.core.models import Entity, Buy_Link
from apps.core.tasks.entity import fetch_image
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.management.decorators import staff_only


log = getLogger('django')


class EntityListView(FilterMixin, ListView):
    template_name = 'management/entities/list.html'
    model = Entity
    paginate_by = 30
    context_object_name = 'entities'
    paginator_class = ExtentPaginator

    def get_queryset(self):
        qs = super(EntityListView, self).get_queryset()
        status = self.request.GET.get('status', None)
        if status is None:
            return qs
        else:
            entity_list = qs.filter(status=int(status)).order_by(
                    '-updated_time')
        return entity_list

    # TODO: need clear input  in filter Mixin
    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'brand':
            qs = qs.filter(brand__icontains=filter_value.strip())
        elif filter_field == 'title':
            qs = qs.filter(title__icontains=filter_value.strip())
        else:
            pass
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(EntityListView, self).get_context_data(*args, **kwargs)
        context['status'] = self.request.GET.get('status', None)
        return context


@login_required
@staff_only
def list(request, template='management/entities/list.html'):
    status = request.GET.get('status', None)
    page = request.GET.get('page', 1)

    if status is None:
        entity_list = Entity.objects.all()
    else:
        entity_list = Entity.objects.filter(status=int(status)).order_by(
                '-updated_time')

    paginator = ExtentPaginator(entity_list, 30)

    try:
        entities = paginator.page(page)
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        raise Http404
    return render_to_response(
            template,
            {
                'entities': entities,
                'status': status,
            },
            context_instance=RequestContext(request)
    )


@login_required
@staff_only
def edit(request, entity_id, template='management/entities/edit.html'):
    _update = None
    try:
        entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    data = {
        'creator': entity.user.profile.nickname,
        'brand': entity.brand,
        'title': entity.title,
        'price': entity.price,
        'status': entity.status,
        'category': entity.category.group_id,
        'sub_category': entity.category_id,
    }

    if request.method == "POST":
        _forms = EditEntityForm(
                entity,
                request.POST,
                initial=data
        )
        _update = 1

        if _forms.is_valid():
            _forms.save()
            _update = 0

    else:
        _forms = EditEntityForm(
                entity=entity,
                initial=data
        )

    return render_to_response(
            template,
            {
                'entity': entity,
                'forms': _forms,
                'update': _update,
            },
            context_instance=RequestContext(request)
    )


@login_required
@staff_only
def create(request, template='management/entities/new.html'):
    _url = request.GET.get('url')

    if _url is None:
        raise Http404
    res = load_entity_info(_url)

    if res.has_key('entity_id'):
        return HttpResponseRedirect(
                reverse('management_entity_edit', args=[res['entity_id']]))

    if len(res) == 0:
        return HttpResponse('not support')

    if request.method == "POST":
        _forms = CreateEntityForm(request=request, data=request.POST,
                                  initial=res)
        if _forms.is_valid():
            entity = _forms.save()
            return HttpResponseRedirect(
                    reverse('management_entity_edit', args=[entity.pk]))
    else:

        key_string = "%s%s" % (res['cid'], res['origin_source'])
        key = md5(key_string.encode('utf-8')).hexdigest()
        category_id = cache.get(key)
        if category_id:
            res['category_id'] = category_id
        else:
            res['category_id'] = 300
        _forms = CreateEntityForm(request=request, initial=res)

    return render_to_response(
            template,
            {
                'res': res,
                'forms': _forms,
            },
            context_instance=RequestContext(request)
    )


# TODO:
'''
    Handle Entity Buy Link
'''


@login_required
@staff_only
def buy_link(request, entity_id, template='management/entities/buy_link.html'):
    # _buy_link_list = Buy_Link.objects.filter(entity_id = entity_id)
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        _forms = BuyLinkForm(entity=_entity, data=request.POST)
        # log.info(request.POST)
        if _forms.is_valid():
            _forms.save()
            return HttpResponseRedirect(
                    reverse('management_entity_edit', args=[entity_id]))
    else:
        _forms = BuyLinkForm(entity=_entity)

    return render_to_response(
            template,
            {
                'entity': _entity,
                'forms': _forms,
                # 'buy_link_list': _buy_link_list,
            },
            context_instance=RequestContext(request)
    )


@csrf_exempt
@login_required
def edit_buy_link(request, bid,
                  template='management/entities/edit_buy_link.html'):
    try:
        buy = Buy_Link.objects.get(pk=bid)
    except Buy_Link.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        _forms = EditBuyLinkForm(buy_link=buy, data=request.POST)
        if _forms.is_valid():
            buy_link = _forms.save()
            return HttpResponseRedirect(
                    reverse('management_entity_edit',
                            args=[buy_link.entity_id]))
    else:
        # log.info(int(buy.default))
        _forms = EditBuyLinkForm(buy_link=buy, initial={
            'link': buy.link,
            'default': buy.default,
        })

    return render_to_response(
            template,
            {
                'entity': buy.entity,
                'forms': _forms,
            },
            context_instance=RequestContext(request))


@csrf_exempt
@login_required
@staff_only
def remove_buy_link(request, bid):
    try:
        b = Buy_Link.objects.get(pk=bid)
    except Buy_Link.DoesNotExist:
        return ErrorJsonResponse(status=404)

    if b.default:
        return ErrorJsonResponse(status=403)
    b.delete()
    return SuccessJsonResponse()


@csrf_exempt
@login_required
@staff_only
def check_buy_link(request, bid):
    try:
        b = Buy_Link.objects.get(pk=bid)
    except Buy_Link.DoesNotExist:
        return ErrorJsonResponse(status=404)

    # def crawl(item_id):
    data = {
        'project': 'default',
        'spider': 'taobao',
        'setting': 'DOWNLOAD_DELAY=2',
        'item_id': b.origin_id,
    }
    res = requests.post('http://10.0.2.48:6800/schedule.json', data=data)
    # return res.json()
    return SuccessJsonResponse(data=res.json())


# TODO:
'''
    Handle Image
'''


@login_required
@staff_only
def refetch_image(request, entity_id):
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    log.info(_entity.images)

    fetch_image(_entity.images, _entity.pk)
    return SuccessJsonResponse(data={'status': 'ok'})


@login_required
def image(request, entity_id,
          template='management/entities/upload_image.html'):
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = EntityImageForm(entity=_entity, data=request.POST,
                                 files=request.FILES)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = EntityImageForm(entity=_entity)

    return render_to_response(
            template,
            {
                'entity': _entity,
                'forms': _forms,
            },
            context_instance=RequestContext(request)
    )


@csrf_exempt
@login_required
def delete_image(request, entity_id):
    if request.method == 'POST':
        _index = request.POST.get('index', None)
        log.info(_index)
        try:
            _entity = Entity.objects.get(pk=entity_id)
            images = _entity.images
            log.info(images)
            images.remove(_index)
            _entity.images = images
            _entity.save()
        except Entity.DoesNotExist:
            raise Http404

        status = True
        # if 'http://imgcdn.guoku.com/' in _index:
        #     image_name = _index.replace('http://imgcdn.guoku.com/', '')
        #     status = default_storage.delete(image_name)
        return SuccessJsonResponse(data={'status': status})

    return HttpResponseNotAllowed


__author__ = 'edison7500'
