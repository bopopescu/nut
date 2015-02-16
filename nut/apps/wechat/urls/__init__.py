from django.conf.urls import url, patterns, include
from apps.wechat.views import WeChatView
from apps.wechat.views.bind import WeChatBindView


urlpatterns = patterns(
    'apps.wechat.views',
    url(r'^$', WeChatView.as_view(), name='wechat_index'),
    url(r'^menu/', include('apps.wechat.urls.meun')),
    # url(r'^bind/', include('apps.wechat.urls.bind')),

    url(r'^bind/(?P<open_id>.*)/$', WeChatBindView.as_view(), name='wechat_bind'),
    url(r'^bind/success/$', WeChatBindView.as_view(), name='wechat_bind_success'),
)


__author__ = 'edison'
