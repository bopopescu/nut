# encoding: utf-8
import json
from apps.core.utils.http import JSONResponse
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
from apps.core.models import Entity
from apps.order.models import SKU,Order
from django.template import RequestContext
from django.views.generic import ListView, CreateView, DeleteView, UpdateView,DetailView, View
from django.http import Http404

class MyOrderUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        idlist=[9020,1997153,2000859,1964551]
        return user.id in idlist
    def no_permissions_fail(self, request=None):
        raise Http404
class IndexView(MyOrderUserPassesTestMixin,ListView):
    model = Order
    template_name = 'web/checkout/index.html'
    def get(self,request,*args,**kwargs):
        self.object_list = self.get_queryset()
        number=self.request.GET.get('filtervalue','')
        if number:
            return HttpResponseRedirect(reverse('checkout_order_list')+'?number='+str(number))
        else:
            context = self.get_context_data()
            return self.render_to_response(context)
    def get_queryset(self):
        return Order.objects.none()

class AllOrderListView(MyOrderUserPassesTestMixin,FilterMixin, SortMixin,ListView):
    default_sort_params = ('created_datetime', 'desc')
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/allorder.html'
    def get(self,request,*args,**kwargs):
        self.object_list = self.get_queryset()
        number=self.request.GET.get('filtervalue','')
        if number:
            return HttpResponseRedirect(reverse('checkout_order_list')+'?number='+str(number))
        else:
            context = self.get_context_data()
            return self.render_to_response(context)
    def get_queryset(self):
        qs = Order.objects.all()
        return self.sort_queryset(qs, *self.get_sort_params())

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'created_datetime':
            qs = qs.order_by('-created_datetime')
            return qs

class SellerOrderListView(MyOrderUserPassesTestMixin,FilterMixin, SortMixin,ListView):
    default_sort_params = ('created_datetime', 'desc')
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/orderlists.html'
    def get_queryset(self):
        qs = Order.objects.all()
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        order_number = self.request.GET.get('number')
        filter_field, filter_value = filter_param
        #if filter_field == 'id':
            #qs = qs.filter(id=filter_value.strip())
        if filter_field == 'number':
            qs = qs.filter(number__icontains=filter_value.strip())
        elif order_number:
            qs=qs.filter(number__icontains=order_number.strip())
        return qs
    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'created_datetime':
            qs = qs.order_by('-created_datetime')
        return qs

    def get_context_data(self, **kwargs):
        context = super(SellerOrderListView, self).get_context_data(**kwargs)
        context['input_value'] = self.request.GET.get('number')
        context['filter_input_value'] = self.request.GET.get('filtervalue','')
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count=order.items.all().count()
            order.itemslist=order.items.all()[1:order.count]
        return context

class SellerOrderDeleteView(MyOrderUserPassesTestMixin,DeleteView):
    model = Order
    template_name = 'web/checkout/delete_order.html'
    pk_url_kwarg = 'order_number'
    def get_success_url(self):
        return reverse('checkout_order_list')


class CheckoutView(MyOrderUserPassesTestMixin, AjaxResponseMixin,UpdateView):
    model = Order
    template_name = 'web/seller_management/sku/sku_edit_template.html'
    http_method_names = ["post"]
    def post_ajax(self, request, *args, **kwargs):
        order_id=request.POST['order_id']
        instance = Order.objects.get(pk=order_id)
        instance.status='3'
        try:
            instance.save()
            return JSONResponse(data={'result':1},status=200)
        except Exception:
            return JSONResponse(data={'result':0},status=400)

