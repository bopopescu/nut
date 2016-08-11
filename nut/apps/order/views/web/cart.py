#encoding=utf-8
from braces.views import LoginRequiredMixin, AjaxResponseMixin,JSONRequestResponseMixin
from django.core.urlresolvers import reverse
from django.views.generic import ListView,TemplateView, View
from django.shortcuts import redirect, get_object_or_404
from django.http import  Http404

from apps.order.models import SKU
from apps.order.exceptions import OrderException


class UserCartView(LoginRequiredMixin, ListView):
    template_name = 'web/cart/cart.html'
    context_object_name = 'cart_items'

    def get_login_url(self):
        return reverse('web_login')

    def get_queryset(self):
        return self.request.user.cart_items.all()


class UserCheckoutView(LoginRequiredMixin,TemplateView):
    template_name = 'web/cart/checkout.html'
    def get_login_url(self):
        return reverse('web_login')

    def get_context_data(self, **kwargs):
        #key
        context = super(UserCheckoutView,self).get_context_data()
        order = None
        if self.request.user.cart_item_count <= 0:
            context['message'] = '购物车为空,请添加商品之后结算'
            return context
        try:
            order = self.request.user.checkout()
        except OrderException as e :
            context['message'] = '创建订单失败'
            return context

        context['order'] = order
        return context


    def get(self, *args, **kwargs):
        context =  self.get_context_data()
        order = context.get('order', None)
        if order:
            return redirect('web_user_order', pk=order.id)
        else:
            context['message'] = '不明错误'
        return super(UserCheckoutView,self).get(*args, **kwargs)



class UserAddSKUView(LoginRequiredMixin,
                        AjaxResponseMixin,
                        JSONRequestResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        data = self.get_request_json()
        sku_id = data.get('sku_id', None)
        volume = data.get('volume', 1)
        sku = self.get_sku_by_id(sku_id)

        if sku:
            card_item = self.request.user.add_sku_to_cart(sku=sku, volume=volume)
            return self.render_json_response({'status':'success', 'volume': card_item.volume}, 200)

        else:
            return self.render_json_response({'status':'error'}, 404)

    def get_sku_by_id(self, sku_id):
        return get_object_or_404(SKU, pk=sku_id)

