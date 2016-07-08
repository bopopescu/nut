from django.conf.urls import url, patterns
from apps.management.views.users import MediaListView, \
                                        UserAuthorSetView,\
                                        UserAuthorInfoEditView,\
                                        UserManagementListView,\
                                        UserSellerSetView,\
                                        SellerShopListView,\
                                        SellerShopCreateView,\
                                        SellerShopUpdateView,\
                                        SellerShopDeleteView, UserActiveUserSetView,\
                                        SellerEntityListView

urlpatterns = patterns(
    'apps.management.views.users',
    url(r'^$', UserManagementListView.as_view(), name='management_user_list'),
    url(r'^(?P<active>\w+)/$', UserManagementListView.as_view(), name='management_user_list_status'),
    url(r'^(?P<user_id>\d+)/edit/$', 'edit', name='management_user_edit'),
    url(r'^(?P<user_id>\d+)/media/$', MediaListView.as_view(), name='management_user_media'),
    url(r'^(?P<user_id>\d+)/reset-password/$', 'reset_password', name='management_user_reset_password'),
    url(r'^(?P<user_id>\d+)/upload-avatar/$', 'upload_avatar', name='management_user_upload_avatar'),
    url(r'^(?P<user_id>\d+)/post/$', 'post', name='management_user_post'),
    url(r'^(?P<user_id>\d+)/notes/$', 'notes', name='management_user_notes'),

    # for user group setting ajax call
    url(r'^(?P<user_id>\d+)/setAuthor/$', UserAuthorSetView.as_view(), name='management_user_setAuthor'),
    url(r'^(?P<user_id>\d+)/setSeller/$', UserSellerSetView.as_view(), name='management_user_setSeller'),
    url(r'^(?P<user_id>\d+)/setActiveUser/$', UserActiveUserSetView.as_view(), name='management_user_setActiveUser'),

    url(r'^(?P<user_id>\d+)/editAuthorInfo/$', UserAuthorInfoEditView.as_view(), name='management_user_editAuthor'),
    url(r'^(?P<user_id>\d+)/entities/$',SellerEntityListView.as_view(),name='management_user_entity_list'),
    # for seller shop management
    url(r'^(?P<user_id>\d+)/shops/$', SellerShopListView.as_view(), name='management_user_shop_list'),
    url(r'^(?P<user_id>\d+)/shops/new/$', SellerShopCreateView.as_view(), name='management_user_shop_create'),
    url(r'^(?P<user_id>\d+)/shops/(?P<shop_id>\d+)/update/$', SellerShopUpdateView.as_view(), name='management_user_shop_update'),
    url(r'^(?P<user_id>\d+)/shops/(?P<shop_id>\d+)/delete/$', SellerShopDeleteView.as_view(), name='management_user_shop_delete'),

)

__author__ = 'edison'
