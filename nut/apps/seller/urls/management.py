from django.conf.urls import url, patterns

from apps.seller.views.management import SellerCreateView, \
                                         SellerListView, \
                                         SellerUpdateView,\
                                         Store2016IndexManageView

urlpatterns = patterns(
    'apps.seller.views.management',
    url(r'^$', SellerListView.as_view() , name="management_seller_list"),
    url(r'^edit/(?P<pk>\d+)/$', SellerUpdateView.as_view() , name='management_seller_update'),
    url(r'^new/$', SellerCreateView.as_view() , name='management_seller_create'),
    url(r'^meta_2016/$', Store2016IndexManageView.as_view(), name='management_2016_store_index'),


)