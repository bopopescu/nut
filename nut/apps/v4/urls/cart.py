from django.conf.urls import url, patterns
from apps.v4.views.orders.cart import CartListView, AddSKUToCartView, \
                                    ClearCartView, IncrCartItemView, \
                                    DescCartItemView, CheckOutView


urlpatterns = patterns(
    'apps.v4.views.orders.cart',
    url(r'^$', CartListView.as_view(), name='v4_cart_list'),
    url(r'^add/$', AddSKUToCartView.as_view(), name='v4_add_to_cart'),
    url(r'^incr/$', IncrCartItemView.as_view(), name='v4_incr_cart'),
    url(r'^desc/$', DescCartItemView.as_view(), name='v4_desc_cart'),
    url(r'^clear/$', ClearCartView.as_view(), name='v4_clear_cart'),

    url(r'^checkout/$', CheckOutView.as_view(), name='v4_checkout_shopping_cart')
)