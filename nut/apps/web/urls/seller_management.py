from apps.management.views.entities import EntitySKUCreateView
from apps.web.views.seller_management import SellerManagement, SellerManagementAddEntity,\
                                             SKUListView,SKUCreateView,SKUDeleteView,SKUUpdateView, \
                                             SellerEntitySKUCreateView
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.seller_management',

    url(r'^$', SellerManagement.as_view(), name='web_seller_management'),
    url(r'^entity_list/$', SellerManagement.as_view()),
    url(r'^add_entity/$', SellerManagementAddEntity.as_view(), name='web_seller_management_entity_add'),
    url(r'^(?P<entity_id>\d+)/new/$', SellerEntitySKUCreateView.as_view(), name='web_seller_management_entity_sku_create'), #Todo modify url
    url(r'^(?P<entity_id>\d+)/new/$', EntitySKUCreateView.as_view(), name='management_entity_sku_create'),
    url(r'^(?P<entity_id>\d+)/skus/$', SKUListView.as_view(), name='sku_list_management'),
    url(r'^(?P<entity_id>\d+)/skus/new/$', SKUCreateView.as_view(), name='add_sku_management'),
    url(r'^(?P<entity_id>\d+)/skus/(?P<pk>\d+)/delete/$', SKUDeleteView.as_view(), name='sku_delete_management'),
    url(r'^(?P<entity_id>\d+)/skus/(?P<pk>\d+)/update/$', SKUUpdateView.as_view(), name='sku_update_management'))
