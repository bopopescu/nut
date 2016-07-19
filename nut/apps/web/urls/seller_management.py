from apps.management.views.entities import EntitySKUCreateView
from apps.web.views.seller_management import SellerManagement, SellerManagementAddEntity
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.seller_management',

    url(r'^$', SellerManagement.as_view(), name='web_seller_management'),
    url(r'^entity_list/$', SellerManagement.as_view()),
    url(r'^add_entity/$', SellerManagementAddEntity.as_view(), name='web_seller_management_entity_add'),
    url(r'^(?P<entity_id>\d+)/new/$', EntitySKUCreateView.as_view(), name='management_entity_sku_create'))