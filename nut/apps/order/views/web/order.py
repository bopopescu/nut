from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import get_object_or_404
from apps.order.models import Order

class UserOrderListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return self.request.user.orders.all()

class UserOrderView(LoginRequiredMixin, DetailView):
    context_object_name = 'order'
    template_name = 'web/order/order_detail.html'

    def get_login_url(self):
        return reverse('web_login')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        return  get_object_or_404(Order, user=self.request.user, pk=pk)
