from django.conf.urls import url, patterns
from apps.management.views.wechat import RobotListView, MsgCreateView


urlpatterns = patterns(
    'apps.management.views.wechat',
    url(r'^$', RobotListView.as_view(), name='management_wechat_robots'),
    url(r'^create/$', '', name='management_wechat_msg_create'),
)

__author__ = 'edison7500'
