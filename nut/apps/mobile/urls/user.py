from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.user',
    url(r'^(?P<user_id>\d+)/tag/(?P<tag>\w+)/$', 'tag_detail', name='mobile_user_tag_detail'),
    url(r'^user/(?P<user_id>\d+)/like/$', 'entity_like', name='mobile_user_entity_like'),
)


__author__ = 'edison7500'
