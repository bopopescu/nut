
from apps.web.views.seller_management import SKUListView,SKUCreateView,SKUDeleteView,SKUUpdateView, \
                                             SellerManagementEntitySave,OrderDetailView,\
                                             SellerManagementOrders, SellerManagementSoldEntityList, \
                                             SellerManagementSkuSave, SellerManagementImportEntity
from apps.web.views.seller_management import SellerManagement, SellerManagementAddEntity
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.seller_management',

    url(r'^$', SellerManagement.as_view(), name='web_seller_management'),
    url(r'^entity_list/$', SellerManagement.as_view()),
    url(r'^orders/$', SellerManagementOrders.as_view(), name='web_seller_management_order_list'),
    url(r'^sold_entity/$', SellerManagementSoldEntityList.as_view(), name='web_seller_management_sold_entity_list'),
    url(r'^sku_save/$', SellerManagementSkuSave.as_view(), name='web_seller_management_sku_save'),
    url(r'^add_entity/$', SellerManagementAddEntity.as_view(), name='web_seller_management_entity_add'),
    url(r'^import_entity/$', SellerManagementImportEntity.as_view()),
    url(r'^(?P<entity_id>\d+)/edit/$', 'seller_management_entity_edit', name='web_seller_management_entity_edit'),
    url(r'^(?P<entity_id>\d+)/save/$', SellerManagementEntitySave.as_view(), name='web_seller_management_entity_save'),
    url(r'^(?P<entity_id>\d+)/skus/$', SKUListView.as_view(), name='sku_list_management'),
    url(r'^(?P<entity_id>\d+)/skus/new/$', SKUCreateView.as_view(), name='add_sku_management'),
    url(r'^orders/(?P<order_number>\d+)/detail/$',OrderDetailView.as_view(),name='order_detail_management'),
    url(r'^(?P<entity_id>\d+)/skus/(?P<pk>\d+)/delete/$', SKUDeleteView.as_view(), name='sku_delete_management'),
    url(r'^(?P<entity_id>\d+)/skus/(?P<pk>\d+)/update/$', SKUUpdateView.as_view(), name='sku_update_management'))


