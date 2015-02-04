from django.conf.urls import url, patterns
from apps.wechat.views import WeChatView

urlpatterns = patterns(
    'apps.wechat.views',
    url(r'^$', WeChatView.as_view(), name='wechat_index'),

)


__author__ = 'edison'
