from django.conf.urls import url, patterns, include
from apps.notifications.management import DailyPushListView, DailyPushCreateView

urlpatterns = patterns(
    'apps.notifications.views',
    # url(r'^$', 'messages', name='web_messages'),
    url(r'^$', DailyPushListView.as_view(), name='management_push_list'),
    url(r'^new/$', DailyPushCreateView.as_view(), name='management_push_create'),
    url(r'^(?P<pk>\d+)/delete/$', DailyPushCreateView.as_view(), name='management_push_create'),
)


