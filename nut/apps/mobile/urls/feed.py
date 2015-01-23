from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.feed',
    url(r'^$', 'activity', name='mobile_user_activity'),
)

__author__ = 'edison'
