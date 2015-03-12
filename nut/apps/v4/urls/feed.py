from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.v4.views.feed',
    url(r'^$', 'activity', name='mobile_user_activity'),
)

__author__ = 'edison'
