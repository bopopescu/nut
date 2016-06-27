from django.conf.urls import url, patterns, include

from apps.wechat.views.management import KeywordListView, KeywordCreateView, KeywordDeleteView


urlpatterns = patterns(
    '',
    url(r'^$', KeywordListView.as_view(), name='management_wechat_keyword_list'),
    url(r'^new/$', KeywordCreateView.as_view(), name='management_wechat_keyword_create'),
    url(r'^(?P<pk>.*)/delete/$', KeywordDeleteView.as_view(), name='management_wechat_keyword_delete'),

)