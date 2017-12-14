from hashlib import md5

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.utils.log import getLogger
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, CreateView, UpdateView
from django.views.generic import View
from django.views.generic.list import ListView

from apps.core.extend.paginator import ExtentPaginator as Jpaginator
from apps.core.forms.entity import EditEntityForm, EntityImageForm, \
    CreateEntityForm, load_entity_info, BuyLinkForm, EditBuyLinkForm, AddEntityForm
from apps.core.mixins.views import FilterMixin
from apps.core.models import Entity, Buy_Link, GKUser
from apps.core.tasks.entity import fetch_image
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.management.decorators import staff_and_editor
from apps.management.forms.sku import SKUForm
from apps.management.mixins.auth import EditorRequiredMixin
from apps.order.models import SKU


log = getLogger('django')
image_host = getattr(settings, 'IMAGE_HOST', None)


class EntityListView(FilterMixin, ListView):
    template_name = 'management/entities/list.html'
    model = Entity
    paginate_by = 30
    context_object_name = 'entities'
    paginator_class = Jpaginator

    def get_amazon_entities(self, qs):
        amazon_entity_ids = Buy_Link.objects \
            .filter(origin_source__icontains='amazon') \
            .values_list('entity_id', flat=True)
        return qs.filter(pk__in=amazon_entity_ids)

    def get_queryset(self):
        qs = super(EntityListView, self).get_queryset()
        status = self.request.GET.get('status', None)
        if status is None:
            return qs
        elif status == '999':
            entity_list = self.get_amazon_entities(qs)
        elif status == '888':
            entity_list = self.get_editor_frozen_entities(qs)
        elif status == '666':
            entity_list = self.get_active_user_entities(qs)
        else:
            entity_list = qs.filter(status=int(status)).order_by('-updated_time')
        return entity_list

    def get_active_user_entities(self, qs):
        active_users = GKUser.objects.active_user()
        entity_list = Entity.objects \
            .filter(user__in=active_users) \
            .order_by('-updated_time')
        return entity_list

    def get_editor_frozen_entities(self, qs):
        editors = GKUser.objects.editor()
        entity_frozen = Entity.objects \
            .filter(status=Entity.freeze, user__in=editors) \
            .order_by('-updated_time')
        return entity_frozen

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

    @staff_and_editor
    def dispatch(self, request, *args, **kwargs):
        return super(EntityListView, self).dispatch(request, *args, **kwargs)


@login_required
@staff_and_editor
def edit(request, entity_id, template='management/entities/edit.html'):
    _update = None
    try:
        entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    data = {
        # 'id':entity.pk,
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
        # log.info(entity.category)
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
@staff_and_editor
def create(request, template='management/entities/new.html'):
    _url = request.GET.get('url')

    if _url is None:
        raise Http404
        # print(_url)
    res = load_entity_info(_url)
    # log.info("OKOKO %s", len(res))

    if res.has_key('entity_id'):
        return HttpResponseRedirect(
            reverse('management_entity_edit', args=[res['entity_id']]))

    if len(res) == 0:
        return HttpResponse('not support')

    if request.method == "POST":
        # log.info(request.POST)
        _forms = CreateEntityForm(request=request, data=request.POST,
                                  initial=res)
        # _forms = EntityURLFrom(request=request, data=request.POST)
        if _forms.is_valid():
            entity = _forms.save()
            return HttpResponseRedirect(
                reverse('management_entity_edit', args=[entity.pk]))
    else:

        # log.info("category %s %s" % (res['cid'], res['origin_source']))
        key_string = "%s%s" % (res['cid'], res['origin_source'])
        # log.info(ke)
        key = md5(key_string.encode('utf-8')).hexdigest()
        category_id = cache.get(key)
        # res.update('category_id', category_id)
        if category_id:
            res['category_id'] = category_id
        else:
            res['category_id'] = 300
        # log.info("%s %s" % (key, category_id))
        _forms = CreateEntityForm(request=request, initial=res)

    return render_to_response(
        template,
        {
            'res': res,
            'forms': _forms,
        },
        context_instance=RequestContext(request)
    )


class ImportEntity(View):
    def __init__(self, template='management/entities/new.html', entity_edit_url='management_entity_edit',
                 form=CreateEntityForm, **kwargs):
        self.template = template
        self.entity_edit_url = entity_edit_url
        self.form = form
        super(ImportEntity, self).__init__(**kwargs)

    @staticmethod
    def get_res(request):
        _url = request.GET.get('url')
        if _url is None:
            raise Http404
        return load_entity_info(_url)

    def get(self, request, *args, **kwargs):
        res = ImportEntity.get_res(request)
        if not res:
            return HttpResponse('not support')
        if 'entity_id' in res:
            # entity already exists
            return HttpResponseRedirect(reverse(self.entity_edit_url, args=[res['entity_id']]))
        else:
            key_string = "%s%s" % (res['cid'], res['origin_source'])
            key = md5(key_string.encode('utf-8')).hexdigest()
            category_id = cache.get(key)
            if category_id:
                res['category_id'] = category_id
            else:
                res['category_id'] = 300
            _forms = self.form(request=request, initial=res)
            return render(request, self.template, {'res': res, 'forms': _forms})

    def post(self, request, *args, **kwargs):
        res = ImportEntity.get_res(request)
        _forms = self.form(request=request, data=request.POST, initial=res)
        if _forms.is_valid():
            entity = _forms.save()
            return HttpResponseRedirect(reverse(self.entity_edit_url, args=[entity.pk]))


class Add_local(View):
    template_name = 'management/entities/add.html'
    form_class = AddEntityForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request)
        return render(request, self.template_name, {'forms': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('management_entity_list'))
        return render(request, self.template_name, {'forms': form})


@login_required
@staff_and_editor
def buy_link(request, entity_id, template='management/entities/buy_link.html'):
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        _forms = BuyLinkForm(entity=_entity, data=request.POST)
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
        },
        context_instance=RequestContext(request)
    )


@csrf_exempt
@login_required
@staff_and_editor
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
                reverse('management_entity_edit', args=[buy_link.entity_id]))
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
@staff_and_editor
def remove_buy_link(request, bid):
    try:
        b = Buy_Link.objects.get(pk=bid)
    except Buy_Link.DoesNotExist:
        return ErrorJsonResponse(status=404)

    if b.default:
        return ErrorJsonResponse(status=403)
    b.delete()
    return SuccessJsonResponse()


class CheckBuyLinkView(View):
    # http_method_names = ['GET']

    def get_context_data(self, **kwargs):
        try:
            b = Buy_Link.objects.get(pk=self.bid)
        except Buy_Link.DoesNotExist:
            raise Http404

        data = {
            'project': 'default',
            'spider': 'taobao',
            'setting': 'DOWNLOAD_DELAY=2',
            'item_id': b.origin_id,
        }
        res = requests.post(settings.CHECK_BUY_LINK_URL, data=data)
        if res.status_code == 200:
            return SuccessJsonResponse(data=res.json())
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        self.bid = kwargs.pop('bid', None)
        assert self.bid is not None
        return self.get_context_data(**kwargs)

    @staff_and_editor
    def dispatch(self, request, *args, **kwargs):
        return super(CheckBuyLinkView, self).dispatch(request, *args, **kwargs)


# TODO:
'''
    Handle Image
'''


@login_required
@staff_and_editor
def refetch_image(request, entity_id):
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    log.info(_entity.images)

    fetch_image(_entity.images, _entity.pk)
    return SuccessJsonResponse(data={'status': 'ok'})


@login_required
@staff_and_editor
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
            return HttpResponseRedirect(reverse('management_entity_edit', args=[_entity.id]))

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
@staff_and_editor
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
        return SuccessJsonResponse(data={'status': status})

    return HttpResponseNotAllowed


class EntitySKUListView(EditorRequiredMixin, ListView):
    template_name = 'management/entities/entity_sku_list.html'

    def get_queryset(self):
        entity = self.get_entity()
        return entity.skus.all()

    def get_entity(self):
        return get_object_or_404(Entity, id=self.kwargs.get('entity_id', None))

    def get_context_data(self, **kwargs):
        context = super(EntitySKUListView, self).get_context_data(**kwargs)
        context['entity'] = self.get_entity()
        return context


class EntitySKUCreateView(EditorRequiredMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'management/entities/create_sku.html'

    def get_success_url(self):
        return reverse('management_entity_skus', args=[self.get_entity().id])

    def get_initial(self):
        entity = self.get_entity()
        return {
            'entity': entity.id
        }

    def get_entity(self):
        entity_id = self.kwargs.get('entity_id')
        entity = get_object_or_404(Entity, id=entity_id)
        return entity

    def get_context_data(self, **kwargs):
        context = super(EntitySKUCreateView, self).get_context_data(**kwargs)
        context['entity'] = self.get_entity()
        context['entity_id'] = self.get_entity().id
        return context


class EntitySKUUpdateView(EditorRequiredMixin, UpdateView):
    model = SKU
    form_class = SKUForm
    template_name = 'management/entities/update_sku.html'

    def get_entity(self):
        entity_id = self.kwargs.get('entity_id')
        entity = get_object_or_404(Entity, id=entity_id)
        return entity

    def get_context_data(self, **kwargs):
        context = super(EntitySKUUpdateView, self).get_context_data(**kwargs)
        context['entity_id'] = self.get_entity().id
        return context

    def get_success_url(self):
        return reverse('management_entity_skus', args=[self.get_entity().id])


class EntitySKUDeleteView(EditorRequiredMixin, DeleteView):
    model = SKU
    template_name = 'management/entities/delete_sku.html'

    def get_entity(self):
        entity_id = self.kwargs.get('entity_id')
        entity = get_object_or_404(Entity, id=entity_id)
        return entity

    def get_context_data(self, **kwargs):
        context = super(EntitySKUDeleteView, self).get_context_data()
        context['entity'] = self.get_entity()
        return context

    def get_success_url(self):
        return reverse('management_entity_skus', args=[self.get_entity().id])


__author__ = 'edison7500'
