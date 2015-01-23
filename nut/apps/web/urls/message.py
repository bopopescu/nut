from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.web.views.message',
    url(r'^$', 'messages', name='web_messages'),
)

__author__ = 'edison'
