from django.conf.urls import url, patterns, include
from apps.notifications.views import MessageListView, NewMessageListView

urlpatterns = patterns(
    'apps.notifications.views',
    # url(r'^$', 'messages', name='web_messages'),
    url(r'^$', MessageListView.as_view(), name='web_messages'),
    url(r'newmessage/$', NewMessageListView.as_view(), name='web_new_messages'),
)


__author__ = 'edison7500'
