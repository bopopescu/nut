# encoding: utf-8
import json

from braces.views import AjaxResponseMixin, UserPassesTestMixin,JSONResponseMixin
from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DeleteView, UpdateView, View
from django.http import Http404
from django.shortcuts import get_object_or_404

from apps.core.utils.http import JSONResponse
from apps.core.extend.paginator import ExtentPaginator
from apps.core.mixins.views import FilterMixin, SortMixin
from apps.order.models import Order
from apps.payment.models import PaymentLog
from apps.web.forms.checkout import CheckDeskOrderPayForm


class CheckDeskUserTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        return getattr(user, 'is_admin', None)

    def no_permissions_fail(self, request=None):
        raise Http404


class AllOrderListView(CheckDeskUserTestMixin, FilterMixin, SortMixin, ListView):
    default_sort_params = ('created_datetime', 'desc')
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/allorder.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        number = self.request.GET.get('filtervalue', '')
        self.status = self.request.GET.get('status')
        if number:
            if self.status:
                return HttpResponseRedirect(reverse('checkout_order_list')+'?number='+str(number)+'&status='+self.status)
            else:
                return HttpResponseRedirect(reverse('checkout_order_list')+'?number='+str(number))
        else:
            context = self.get_context_data()
            return self.render_to_response(context)

    def get_queryset(self):
        qs = Order.objects.all()
        self.status = self.request.GET.get('status')
        if self.status == 'waiting_for_payment':
            qs = qs.filter(status__in=[1, 2])
        elif self.status == 'paid':
            qs = qs.filter(status__in=[3, 4, 5, 6, 7, 8])
        return self.sort_queryset(qs, *self.get_sort_params())

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'created_datetime':
            qs = qs.order_by('status', '-created_datetime')
            return qs

    def get_context_data(self, **kwargs):
        context = super(AllOrderListView, self).get_context_data(**kwargs)
        context['status']=self.status
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]
        return context


class SellerOrderListView(CheckDeskUserTestMixin, FilterMixin, SortMixin, ListView):
    default_sort_params = ('created_datetime', 'desc')
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/orderlists.html'

    def get_queryset(self):
        qs = Order.objects.all()
        self.status = self.request.GET.get('status')
        if self.status == 'waiting_for_payment':
            qs = qs.filter(status__in=[1, 2])
        elif self.status == 'paid':
            qs = qs.filter(status__in=[3, 4, 5, 6, 7, 8])
        return self.sort_queryset(self.filter_queryset(qs, self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        order_number = self.request.GET.get('number')
        filter_field, filter_value = filter_param
        if filter_value and filter_value != 'all':
            qs = qs.filter(number__icontains=filter_value.strip())
        elif order_number:
            qs=qs.filter(number__icontains=order_number.strip())
        return qs

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'created_datetime':
            qs = qs.order_by('status', '-created_datetime')
        return qs

    def get_context_data(self, **kwargs):
        context = super(SellerOrderListView, self).get_context_data(**kwargs)
        context['input_value'] = self.request.GET.get('number')
        context['filter_input_value'] = self.request.GET.get('filtervalue', '')
        context['status'] = self.status
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]
        return context


class SellerOrderDeleteView(CheckDeskUserTestMixin, DeleteView):

    model = Order
    template_name = 'web/checkout/delete_order.html'
    pk_url_kwarg = 'order_number'

    def get_success_url(self):
        return reverse('checkout_order_list')


class CheckDeskPayView(CheckDeskUserTestMixin, JSONResponseMixin, AjaxResponseMixin, View):

    def get_order(self):
        order_id = int(self.request.POST.get('order_id', None))
        return get_object_or_404(Order, pk=order_id)

    def post_ajax(self, request, *args, **kwargs):
        _form = CheckDeskOrderPayForm(request.POST, request=request)
        if _form.is_valid():
            _form.save()
            return self.render_json_response(
                {
                    'result': 1,
                },
                status=200
            )
        else:
            return self.render_json_response(
                {
                    'result': 0,
                    'message': _form.errors.as_text()
                },
                status=400
            )
