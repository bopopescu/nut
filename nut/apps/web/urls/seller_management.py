from apps.web.views.seller_management import SellerManagement, SellerManagementAddEntity, SellerEntitySKUCreateView
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.seller_management',

    url(r'^$', SellerManagement.as_view(), name='web_seller_management'),
    url(r'^entity_list/$', SellerManagement.as_view()),
    url(r'^add_entity/$', SellerManagementAddEntity.as_view(), name='web_seller_management_entity_add'),
    url(r'^(?P<entity_id>\d+)/new/$', SellerEntitySKUCreateView.as_view(), name='web_seller_management_entity_sku_create')) #Todo modify url