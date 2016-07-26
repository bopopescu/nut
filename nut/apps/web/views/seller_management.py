# encoding: utf-8
import json

from apps.core.extend.paginator import ExtentPaginator
from apps.core.forms.entity import EditEntityForm
from apps.core.mixins.views import FilterMixin, SortMixin
from apps.core.views import LoginRequiredMixin, JSONResponseMixin
from apps.management.views.entities import Add_local
from braces.views import JSONRequestResponseMixin,AjaxResponseMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from apps.management.forms.sku import SKUForm
from apps.core.models import SKU,Entity,Order, GKUser
from django.template import RequestContext
from django.views.generic import ListView, CreateView, DeleteView, UpdateView,DetailView, View
from django.http import Http404

class SKUUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        self.sku_id = self.kwargs.get('pk')
        entity = Entity.objects.get(id = self.entity_id)
        sku = SKU.objects.get(pk=self.sku_id)
        return entity in user.entities.all() and sku in entity.skus.all()
    def no_permissions_fail(self, request=None):
        raise Http404

class EntityUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        entity = Entity.objects.get(id=self.entity_id)
        return entity in user.entities.all()
    def no_permissions_fail(self, request=None):
        raise Http404

class SellerManagement(LoginRequiredMixin, FilterMixin, SortMixin,  ListView):
    default_sort_params = ('price', 'id')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Entity
    paginate_by = 10
    template_name = 'web/seller_management/seller_management.html'

    def get_queryset(self):
        qs = self.request.user.entities.all()
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def get_context_data(self, **kwargs):
        context = super(SellerManagement, self).get_context_data(**kwargs)
        for entity in context['object_list']:
            entity.sku_list = entity.skus.all()
            entity.stock = entity.sku_list.aggregate(Sum('stock')).get('stock__sum', 0) or 0
            entity.title=entity.title[:15]
        context['sort_by'] = self.get_sort_params()[0]
        context['extra_query'] = 'sort_by=' + context['sort_by']
        user = GKUser.objects.get(id=self.request.user.id)
        # skus = user.entities.all()[0].skus.all()
        # sku=user.entities.all().get(id=106020).skus.all()
        # user.add_sku_to_cart(sku[0])
        #user.add_sku_to_cart(skus[1])
        #user.add_sku_to_cart(skus[2])
        # order = user.checkout()

        return context

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'title':
            qs = qs.filter(title__icontains=filter_value.strip())
        else:
            pass
        return qs

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'price':
            qs = qs.order_by('-price')
        else:
            pass
        return qs

class SellerManagementOrders(LoginRequiredMixin, FilterMixin, SortMixin,  ListView):
    default_sort_params = ('id', 'price')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/seller_management/order_list.html'

    def get_queryset(self):
        qs = self.request.user.orders.all()
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'number':
            qs = qs.filter(number__icontains=filter_value.strip())
        else:
            pass
        return qs

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'price':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=True)
        elif sort_by == 'number':
            qs = qs.order_by('-number')
        elif sort_by == 'status':
            qs = qs.order_by('-status')
        else:
            pass
        return qs

    def get_context_data(self, **kwargs):
        context = super(SellerManagementOrders, self).get_context_data(**kwargs)
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]


        return context

class SellerManagementAddEntity(Add_local):
    template_name = 'web/seller_management/add_entity.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web_seller_management'))
        return render(request, self.template_name, {'forms': form})

@login_required
def seller_management_entity_edit(request, entity_id, template='web/seller_management/edit_entity.html'):
    #Todo 拆分模版
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

class SellerManagementEntitySave(AjaxResponseMixin, JSONResponseMixin, View):
    model = Entity
    def save_update(self, price):
        entity = Entity.objects.get(id=self.kwargs.get('entity_id'))
        entity.price = price
        entity.save()
        return

    def post_ajax(self, request, *args, **kwargs):
        price = request.POST.get('price', None)
        price = json.loads(price)
        try:
            self.save_update(price)
        except:
            pass
        return HttpResponseRedirect(reverse('web_seller_management'))

class SellerEntitySKUCreateView(EntityUserPassesTestMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/create_sku.html'
    def get_success_url(self):
        return reverse('management_entity_skus', args=[self.entity_id])    #Todo need change

    def get_initial(self):
        return {
            'entity':self.entity_id
        }

class SKUListView(EntityUserPassesTestMixin, SortMixin, ListView):
    default_sort_params = ('stock', 'origin_price')
    template_name = 'web/seller_management/sku_list.html'
    def get_queryset(self):
        entity = get_object_or_404(Entity, id=self.entity_id)
        return self.sort_queryset(entity.skus.all(), *self.get_sort_params())
    def get_context_data(self, **kwargs):
        context = super(SKUListView, self).get_context_data(**kwargs)
        context['entity']= get_object_or_404(Entity, id=self.entity_id)
        context['sort_by'] = self.get_sort_params()[0]
        context['extra_query'] = 'sort_by=' + context['sort_by']
        return context
    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'stock':
            qs = qs.order_by('-stock')
        elif sort_by == 'origin_price':
            qs = qs.order_by('-origin_price')
        elif sort_by == 'promotion_price':
            qs = qs.order_by('-promo_price')
        elif sort_by == 'status':
            qs = qs.order_by('-status')
        else:
            pass
        return qs


class SKUCreateView(EntityUserPassesTestMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/add_sku.html'
    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])
    def get_context_data(self, **kwargs):
        context = super(CreateView,self).get_context_data(**kwargs)
        context['entity_id']=self.entity_id
        return context
    def get_initial(self):
        return {
            'entity':self.entity_id
        }

class SKUUpdateView(SKUUserPassesTestMixin,UpdateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/update_sku.html'
    def get_context_data(self, **kwargs):
        context = super(SKUUpdateView,self).get_context_data(**kwargs)
        context['entity_id']=self.entity_id
        return context
    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])


class SKUDeleteView(SKUUserPassesTestMixin, DeleteView):
    model = SKU
    template_name = 'web/seller_management/delete_sku.html'

    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])

class OrderDetailView(UserPassesTestMixin,DetailView):
    pk_url_kwarg = 'order_number'
    context_object_name = 'order'
    model = Order
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    paginate_by = 10
    template_name = 'web/seller_management/order_detail.html'
    def test_func(self, user):
        self.order_number = self.kwargs.get('order_number')
        order = Order.objects.get(pk=self.order_number)
        return order in user.orders.all()
    def no_permissions_fail(self, request=None):
        raise Http404
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['order_item'] = context['order'].items.all()
        context['order_number']=self.order_number
        context['promo_total_price']=context['order'].promo_total_price
        context['origin_total_price']=context['order'].grand_total_price
        return context

class SellerManagementSoldEntityList(LoginRequiredMixin, FilterMixin, SortMixin,  ListView):
    default_sort_params = ('price', 'id')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Entity
    paginate_by = 10
    template_name = 'web/seller_management/sold_entity_list.html'

    def get_queryset(self):
        self.order_items = self.request.user.order_items.all()
        qs = list(set([item.sku for item in self.order_items]))
        return self.filter_queryset(qs,self.get_filter_param())

    def get_context_data(self, **kwargs):
        context = super(SellerManagementSoldEntityList, self).get_context_data(**kwargs)
        for sku in context['object_list']:
            sku.title=sku.entity.title[:15]

        d = {}
        for order in self.order_items:
            if order.sku.id not in d.keys():
                d[order.sku.id] = order.volume
            else:
                d[order.sku.id] += order.volume
        for object in context['object_list']:
            object.sold_count = d[object.id]
        context['sort_by'] = self.get_sort_params()[0]
        context['extra_query'] = 'sort_by=' + context['sort_by']
        return context

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'title':
            qs = qs.filter(title__icontains=filter_value.strip())
        else:
            pass
        return qs

class SellerManagementSkuSave(AjaxResponseMixin, JSONResponseMixin, View):
    model = SKU
    def save_update(self, id, price, stock):
        sku = SKU.objects.get(id=id)
        sku.promo_price = price
        sku.stock = stock
        sku.save()
        return

    def post_ajax(self, request, *args, **kwargs):
        price = request.POST.get('price', None)
        id = request.POST.get('id', None)
        stock = request.POST.get('stock', None)
        price = json.loads(price)
        id = json.loads(id)
        stock = json.loads(stock)
        try:
            self.save_update(id, price, stock)
        except:
            pass
        return HttpResponseRedirect(reverse('web_seller_management'))



