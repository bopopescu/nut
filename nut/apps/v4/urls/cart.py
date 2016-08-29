from django.conf.urls import url, patterns
from apps.v4.views.orders.cart import CartListView, AddSKUToCartView



urlpatterns = patterns(
    'apps.v4.views.orders.cart',
    url(r'^$', CartListView.as_view(), name='v4_cart_list'),
    url(r'^add/$', AddSKUToCartView.as_view(), name='v4_add_to_cart'),
)