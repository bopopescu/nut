from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.mobile.views.message',

    url(r'^$', 'message', name='mobile_user_message'),
)

__author__ = 'edison'
