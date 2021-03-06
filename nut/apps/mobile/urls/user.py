from django.conf.urls import url, patterns
from apps.mobile.views.user import APIUserSearchView

urlpatterns = patterns(
    'apps.mobile.views.user',

    url(r'^(?P<user_id>\d+)/$', 'detail', name='mobile_user_info'),
    url(r'^(?P<user_id>\d+)/tag/$', 'tag_list', name='mobile_user_tag_list'),
    url(r'^(?P<user_id>\d+)/tag/(?P<tag>\w+)/$', 'tag_detail', name='mobile_user_tag_detail'),
    url(r'^(?P<user_id>\d+)/like/$', 'entity_like', name='mobile_user_entity_like'),
    url(r'^(?P<user_id>\d+)/entity/note/$', 'entity_note', name='mobile_user_entity_note'),

    url(r'^search/$', APIUserSearchView.as_view(), name='mobile_user_search'),
    url(r'^update/$', 'update', name='mobile_user_update'),

    url(r'^(?P<user_id>\d+)/following/$', 'following_list', name='mobile_user_following'),
    url(r'^(?P<user_id>\d+)/fan/$', 'fans_list', name='mobile_user_fans'),

    url(r'^(?P<user_id>\d+)/follow/(?P<target_status>\d+)/$', 'follow_action', name='mobile_user_follow_action'),
)

__author__ = 'edison7500'
