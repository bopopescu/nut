from django.conf.urls import url, patterns, include
from apps.notifications.views import MessageListView

urlpatterns = patterns(
    'apps.notifications.views',
    # url(r'^$', 'messages', name='web_messages'),
    url(r'^$', MessageListView.as_view(), name='web_messages'),
)


__author__ = 'edison7500'
