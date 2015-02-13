from django.conf.urls import url, patterns, include
from apps.wechat.views import WeChatView

urlpatterns = patterns(
    'apps.wechat.views',
    url(r'^$', WeChatView.as_view(), name='wechat_index'),
    url(r'^menu/', include('apps.wechat.urls.meun')),
    url(r'^bind/', include('apps.wechat.urls.bind')),
)


__author__ = 'edison'
