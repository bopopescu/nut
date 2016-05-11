from django.conf.urls import url, patterns
from apps.management.views.wechat import ReplyListView, CreateReplyView, EditReplyView

urlpatterns = patterns(
    'apps.management.views.wechat',
    url(r'^reply/$', ReplyListView.as_view(), name='management_wechat_reply'),
    url(r'^reply/create/', CreateReplyView.as_view(), name='management_wechat_reply_create'),
    url(r'^reply/(?P<pk>[0-9]+)/$', EditReplyView.as_view(), name='management_wechat_reply_edit'),
)