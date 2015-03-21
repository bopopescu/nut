from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.v4.views.message',

    url(r'^$', 'message', name='v4_user_message'),
)

__author__ = 'edison'
