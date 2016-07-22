from django.conf.urls import url, patterns
from apps.order.views.web.cart import UserCartView, UserCheckoutView, UserAddSKUView
urlpatterns = patterns(
    'apps.order.views.web.cart',
    url(r'^$', UserCartView.as_view(), name='web_user_cart'),
    url(r'^add/$', UserAddSKUView.as_view(), name='web_user_add_sku'),
    url(r'^checkout/$', UserCheckoutView.as_view(), name='web_user_checkout'),
)