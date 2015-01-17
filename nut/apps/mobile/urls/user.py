from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.user',
    url(r'^(?P<user_id>\d+)/tag/(?P<tag>\w+)/$', 'tag_detail', name='mobile_user_tag_detail'),
)


__author__ = 'edison7500'
