from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from apps.order.models import Order


class UserOrderListView(LoginRequiredMixin, ListView):
    template_name = 'web/order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.request.user.orders.all()

class OrderAlipayQrcodeView(DetailView):
    context_object_name = 'order'
    template_name = 'web/order/order_ali_qrcode.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        return get_object_or_404(Order, customer=self.request.user, pk=pk)


class UserOrderView(LoginRequiredMixin, DetailView):
    context_object_name = 'order'
    template_name = 'web/order/order_detail.html'

    def get_login_url(self):
        return reverse('web_login')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        return get_object_or_404(Order, customer=self.request.user, pk=pk)


class OrderWeixinPaymentView(LoginRequiredMixin, DetailView):
    context_object_name = 'order'
    template_name = 'web/order/order_wx_payment.html'

    def get_login_url(self):
        return reverse('web_login')

    def get(self, *args, **kwargs):
        order = self.get_object()
        if order.status >= Order.paid:
            return redirect('web_user_order', pk=order.pk)
        else:
            return super(OrderWeixinPaymentView, self).get(*args, **kwargs)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        return get_object_or_404(Order, customer=self.request.user, pk=pk)
