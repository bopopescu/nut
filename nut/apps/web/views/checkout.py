# encoding: utf-8
import json

from apps.core.extend.paginator import ExtentPaginator
from apps.core.forms.entity import EditEntityForm
from apps.core.mixins.views import FilterMixin, SortMixin
from apps.management.views.entities import Add_local, Import_entity
from apps.order.models import OrderItem
from braces.views import JSONResponseMixin,AjaxResponseMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from apps.management.forms.sku import SKUForm
from apps.core.models import SKU,Entity,Order
from django.template import RequestContext
from django.views.generic import ListView, CreateView, DeleteView, UpdateView,DetailView, View
from django.http import Http404

class MyOrderUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        idlist=[9020,1997153,2000859]
        return user.id in idlist
    def no_permissions_fail(self, request=None):
        raise Http404

class MyOrderListView(MyOrderUserPassesTestMixin,FilterMixin, SortMixin,ListView):
    default_sort_params = ('dnumber', 'desc')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/orderlists.html'
    def get_queryset(self):
        qs = Order.objects.filter(customer_id = self.request.user.id)
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        #if filter_field == 'id':
            #qs = qs.filter(id=filter_value.strip())
        if filter_field == 'number':
            if filter_value == u'1':
                filter_value = 'empty'
            qs = qs.filter(number__icontains=filter_value.strip())
        else:
            pass
        return qs
    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'dprice':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=True)
        elif sort_by == 'uprice':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=False)
        elif sort_by == 'dnumber':
            qs = qs.order_by('-number')
        elif sort_by == 'unumber':
            qs = qs.order_by('number')
        elif sort_by == 'status':
            qs =  qs.order_by('-status')
        else:
            pass
        return qs

    def get_context_data(self, **kwargs):
        context = super(MyOrderListView, self).get_context_data(**kwargs)
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
        return context

class MyOrderDeleteView(MyOrderUserPassesTestMixin,DeleteView):
    model = Order
    template_name = 'web/checkout/delete_order.html'
    pk_url_kwarg = 'order_number'
    def get_success_url(self):
        return reverse('web_my_order_list')

class MyOrderDetailView(MyOrderUserPassesTestMixin,DetailView):
    pk_url_kwarg = 'order_number'
    context_object_name = 'order'
    model = Order
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    paginate_by = 10
    template_name = 'web/checkout/my_order_detail.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        if self.request.GET.get('paid', False):
            if self.status == 1:
                context['order'].set_paid()
            return HttpResponseRedirect(reverse('web_my_order_list'))
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )
    def get_context_data(self, **kwargs):
        self.order_number = self.kwargs.get('order_number')
        context = super(MyOrderDetailView, self).get_context_data(**kwargs)
        self.status=context['order'].status
        context['order_item'] = context['order'].items.all()
        #context['order_item'] = context['order'].items.all()
        context['order_number'] = self.order_number
        context['promo_total_price'] = context['order'].promo_total_price
        context['origin_total_price'] = context['order'].grand_total_price
        context['repetition'] = 0
        return context
