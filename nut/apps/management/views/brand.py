# coding=utf-8
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, View
from django.shortcuts import  redirect, get_object_or_404
from django.utils.log import getLogger

from braces.views import StaffuserRequiredMixin

from apps.core.models import Entity,Brand, Entity_Brand
from apps.core.views import BaseListView, BaseFormView
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage
from apps.management.forms.brand import EditBrandForm, CreateBrandForm

from haystack.query import SearchQuerySet
from apps.core.mixins.views import SortMixin, FilterMixin
from braces.views import JSONRequestResponseMixin,AjaxResponseMixin,StaffuserRequiredMixin



log = getLogger('django')


class BrandStatView(BaseListView):
    template_name = "management/brand/stat.html"

    def get_queryset(self):

        entities_stat = Entity.objects.raw("select id, brand, count(*) as b  from core_entity where brand !='' and status != -1  group by brand ORDER BY b DESC")
        return entities_stat

    def get(self, request):

        _brand_stat_list = self.get_queryset()
        page = request.GET.get('page', 1)

        paginator = ExtentPaginator(list(_brand_stat_list), 30)

        try:
            _brand_stat = paginator.page(page)
        except InvalidPage:
            _brand_stat = paginator.page(1)
        except EmptyPage:
            raise Http404

        context = {
            'brand_stat': _brand_stat,
        }

        return self.render_to_response(context)


class BrandListView(StaffuserRequiredMixin, FilterMixin, ListView):
    template_name = "management/brand/list.html"
    context_object_name = 'brands'
    paginate_by = 30
    paginator_class = ExtentPaginator
    model =  Brand
    # queryset = Brand.objects.all()

    def filter_queryset(self, qs, filter_param):
        filter_field , filter_value = filter_param
        if filter_field == 'brand_name':
            qs = qs.filter(name__icontains=filter_value.strip())
        else:
            pass
        return qs


    def get_queryset(self,*args, **kwargs):
        qs = super(BrandListView, self).get_queryset(*args, **kwargs)
        status = self.request.GET.get('status', None)
        qs = qs.order_by('-status','-score','-icon')

        if not status is None:
            status = int(status)
            if status == Brand.publish:
                qs = qs.filter(status=Brand.publish)
            elif status == Brand.promotion:
                qs = qs.filter(status=Brand.promotion)
            else:
                pass
        return qs

    def get_context_data(self, *args, **kwargs):
        context  = super(BrandListView, self).get_context_data(*args, **kwargs)
        context['status'] =  self.request.GET.get('status', None)
        return context




class BrandEntityListView(BaseListView):
    template_name = 'management/brand/entities.html'
    _brand = u''

    @property
    def brand(self):
        brand = self._brand.split()
        return ''.join(brand)


    def get_queryset(self, **kwargs):
        name = kwargs.pop('brand_name')
        sqs = SearchQuerySet().models(Entity).filter(brand=name)
        return sqs


    def get(self, request, **kwargs):
        self._brand = self.kwargs.get('brand')
        self._brand_id = self.kwargs.get('brand_id')
        assert self._brand is not None
        _entity_list = self.get_queryset(brand_name=self.brand)
        page = request.GET.get('page', 1)

        paginator = ExtentPaginator(_entity_list, 30)

        try:
            _entities = paginator.page(page)
        except InvalidPage:
            _entities = paginator.page(1)
        except EmptyPage:
            raise Http404

        context = {
            'brand': self.brand,
            'entities': _entities,
            'brand_id':self._brand_id,
        }
        return self.render_to_response(context)




class BrandEditView(BaseFormView):
    template_name = 'management/brand/edit.html'

    form_class = EditBrandForm

    def get_form_class(self, **kwargs):
        brand = kwargs.pop('brand')
        k = self.get_form_kwargs()
        k.update(
            {
                'brand':brand
            }
        )
        return self.form_class(**k)

    def get(self, request, brand_id):

        try:
            brand = Brand.objects.get(pk = brand_id)
        except Brand.DoesNotExist:
            raise Http404
        self.initial = brand.toDict()
        log.info(self.initial)

        form = self.get_form_class(brand=brand)
        context = {
            'form': form,
            'brand': brand,
        }
        return self.render_to_response(context)

    def post(self, request, brand_id):
        try:
            brand = Brand.objects.get(pk = brand_id)
        except Brand.DoesNotExist:
            raise Http404

        form = self.get_form_class(brand=brand)
        if form.is_valid():
            brand = form.save()
            return redirect('management_brand_list')


        context = {
            'form':form,
            'brand': brand,
        }
        return self.render_to_response(context)


class BrandNameEditView(BaseFormView):
    template_name = 'management/brand/edit.html'

    form_class = EditBrandForm

    def get_form_class(self, **kwargs):
        brand = kwargs.pop('brand')
        k = self.get_form_kwargs()
        k.update(
            {
                'brand':brand
            }
        )
        return self.form_class(**k)

    def get(self, request, brand_name):

        try:
            brand = Brand.objects.get(name = brand_name)
        except Brand.DoesNotExist:
            raise Http404
        self.initial = brand.toDict()
        log.info(self.initial)
        form = self.get_form_class(brand=brand)
        # log.info(form)
        context = {
            'form': form,
            'brand': brand,
        }
        return self.render_to_response(context)

    def post(self, request, brand_name):
        try:
            brand = Brand.objects.get(name = brand_name)
        except Brand.DoesNotExist:
            raise Http404

        form = self.get_form_class(brand=brand)
        if form.is_valid():
            brand = form.save()

        context = {
            'form':form,
            'brand': brand,
        }
        return self.render_to_response(context)


class BrandCreateView(BaseFormView):

    template_name = 'management/brand/create.html'
    form_class = CreateBrandForm

    def get(self, request):
        form = self.get_form_class()
        context = {
            'form':form,
        }
        return self.render_to_response(context)

    def post(self, request):
        form = self.get_form_class()
        if form.is_valid():
            brand = form.save()
            return HttpResponseRedirect(reverse('management_brand_edit', args=[brand.id]))
        context = {
            'form': form
        }
        return self.render_to_response(context)

class AddBrandEntityView(StaffuserRequiredMixin,AjaxResponseMixin,JSONRequestResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        post_data = self.get_request_json()
        brand_id =  int(post_data.get('brand_id'))
        entity_id = int(post_data.get('entity_id'))
        isBrandEntity = bool(post_data.get('isBrandEntity'))

        try:
            if isBrandEntity:
                Entity_Brand.objects.get_or_create(brand_id=brand_id,entity_id=entity_id)
            else:
                Entity_Brand.objects.filter(brand_id=brand_id, entity_id=entity_id).delete()
        except Exception as e:
            return self.render_json_response({'result':'fail'}, status=500)

        return self.render_json_response({'result':'ok'})

class BrandSelectedEntitiesView(StaffuserRequiredMixin,AjaxResponseMixin, JSONRequestResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        brand_id = self.kwargs.get('brand_id')
        brand = get_object_or_404(Brand, id=brand_id)
        res = []
        for entity in  brand.entities_link.all().order_by('brand_order'):
            entity_dic = {
                'entity_id': entity.entity.id,
                'title': entity.entity.title,
                'cover': entity.entity.chief_image,
                'order': entity.brand_order
            }
            res.append(entity_dic)

        return self.render_json_response({'entities': res})


class SaveSortedEntityView(StaffuserRequiredMixin,AjaxResponseMixin, JSONRequestResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        post_data = self.get_request_json()
        brand_id = post_data.get('brand_id')
        ids = post_data.get('entity_ids')

        try :

            Entity_Brand.objects.filter(brand_id=brand_id).exclude(entity_id__in=ids).delete()
            for index , id in enumerate(ids):

                eb, created = Entity_Brand.objects\
                            .get_or_create(
                                brand_id=brand_id,
                                entity_id=id,
                            )
                eb.brand_order = index
                eb.save()

        except Exception as e :

            return self.render_json_response({'result':'error'}, status=500)

        return self.render_json_response({'result': 'ok'}, status=200)

__author__ = 'edison'
