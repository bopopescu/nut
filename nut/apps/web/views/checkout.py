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
from apps.order.models import Order, OrderItem
from apps.payment.models import PaymentLog
from apps.web.forms.checkout import CheckDeskOrderPayForm


def sum_price(sum, next_log):
    return sum + next_log.order.order_total_value


class CheckDeskUserTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        return getattr(user, 'is_admin', None)

    def no_permissions_fail(self, request=None):
        raise Http404


class CheckDeskAllOrderListView(CheckDeskUserTestMixin, FilterMixin, SortMixin, ListView):
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
        context = super(CheckDeskAllOrderListView, self).get_context_data(**kwargs)
        context['status']=self.status
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]
        return context


class CheckoutOrderListView(CheckDeskUserTestMixin, FilterMixin, SortMixin, ListView):
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
        context = super(CheckoutOrderListView, self).get_context_data(**kwargs)
        context['input_value'] = self.request.GET.get('number')
        context['filter_input_value'] = self.request.GET.get('filtervalue', '')
        context['status'] = self.status
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]
        return context


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


class CheckDeskOrderStatisticView(CheckDeskUserTestMixin, FilterMixin, SortMixin,  ListView):

    default_sort_params = ('dnumber', 'desc')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/order_statistic.html'
    wait_pay_status = [Order.address_unbind, Order.waiting_for_payment]
    paid_status = [Order.paid, Order.send, Order.closed]
    expired_status = [Order.expired]

    def get_queryset(self):
        order_ids = list(OrderItem.objects.values_list('order', flat=True))
        qs = Order.objects.filter(id__in=order_ids)
        self.status = self.request.GET.get('status')

        if self.status == 'waiting_for_payment':
            qs = qs.filter(status__in=self.wait_pay_status)
        elif self.status == 'paid':
            qs = qs.filter(status__in=self.paid_status)

        qs = self.apply_date_filter(qs)
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'number':
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
            qs = qs.order_by('-status')
        else:
            pass
        return qs

    def get_sum_payment(self, order_list):
        sum = 0
        for order in order_list:
            if order.is_paid:
                sum += order.order_total_value
        return sum

    def get_sum_payment_for_payment_source(self, order_list, payment_souce):
        order_ids = list(order_list.values_list('id', flat=True))
        logs = PaymentLog.objects.filter(payment_source=payment_souce, order_id__in=order_ids)
        return reduce(sum_price, list(logs), 0)

    def get_context_data(self, **kwargs):
        context = super(CheckDeskOrderStatisticView, self).get_context_data(**kwargs)
        context['status'] = self.status

        paged_order_list = context['object_list']

        for order in paged_order_list:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]

        order_list = self.get_queryset()
        context['sum_payment_all'] = self.get_sum_payment(order_list)
        context['sum_payment_wx'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.weixin_pay)
        context['sum_payment_ali'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.ali_pay)
        context['sum_payment_cash'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.cash)
        context['sum_payment_credit_card'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.credit_card)
        context['sum_payment_other'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.other)
        return context

    def apply_date_filter(self, order_list):
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        if start_date:
            order_list = order_list.filter(created_datetime__gte=start_date)
        if end_date:
            order_list = order_list.filter(created_datetime__lte=end_date)

        return order_list
