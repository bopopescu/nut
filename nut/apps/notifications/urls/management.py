from django.conf.urls import url, patterns, include
from apps.notifications.management import DailyPushListView, DailyPushCreateView,\
                                          DailyPushSendTestView, DailyPushSendProductionView,\
                                          DailyPushUpdateView,DailyPushDeleteView,\
                                          DailyPushSentListView


urlpatterns = patterns(
    'apps.notifications.management',
    url(r'^$', DailyPushListView.as_view(), name='management_push_list'),
    url(r'^new/$', DailyPushCreateView.as_view(), name='management_push_create'),
    url(r'^(?P<pk>\d+)/delete/$', DailyPushDeleteView.as_view(), name='management_push_delete'),
    url(r'^(?P<pk>\d+)/send_test/$', DailyPushSendTestView.as_view(), name='management_push_send_test'),
    url(r'^(?P<pk>\d+)/send/$', DailyPushSendProductionView.as_view(), name='management_push_send_production'),
    url(r'^(?P<pk>\d+)/update/$', DailyPushUpdateView.as_view(), name='management_push_update'),
    url(r'^sentlist/$', DailyPushSentListView.as_view(), name='management_sent_push_messages'),
)


