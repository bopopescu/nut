from django.conf.urls import url, patterns
# from apps.management.views.entities import EntityListView
from apps.management.views.entities import EntityListView, CheckBuyLinkView
from django.contrib.auth.decorators import login_required


urlpatterns = patterns(
    'apps.management.views.entities',
    # url(r'^$', EntityListView.as_view(), name='management_entity_list'),
    url(r'^$', login_required(EntityListView.as_view()), name='management_entity_list'),
    # url(r'^list/$',EntityListView.as_view() , name='management_entity_list_new'),
    url(r'^new/$', 'create', name='management_entity_create'),
    url(r'^(?P<entity_id>\d+)/edit/$', 'edit', name='management_entity_edit'),

    url(r'^(?P<entity_id>\d+)/buy/link/$', 'buy_link', name='management_entity_buy_link'),
    url(r'^(?P<bid>\d+)/buy/link/remove/$', 'remove_buy_link', name='management_remove_entity_buy_link'),
    url(r'^(?P<bid>\d+)/buy/link/edit/$', 'edit_buy_link', name='management_edit_entity_buy_link'),
    url(r'^(?P<bid>\d+)/buy/link/check/$', login_required(CheckBuyLinkView.as_view()), name='management_check_buy_link'),

    url(r'^image/(?P<entity_id>\d+)/remove/$', 'delete_image', name='management_remove_entity_image'),
    url(r'^image/(?P<entity_id>\d+)/fetch/$', 'refetch_image', name='management_entity_fetch_image'),
    url(r'^image/(?P<entity_id>\d+)/$', 'image', name='management_entity_image'),


)

__author__ = 'edison7500'
