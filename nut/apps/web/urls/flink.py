from django.conf.urls import url, patterns

from apps.web.views.flink import FriendlyLinkListView

urlpatterns = patterns(
    'apps.web.views.flink',
    url(r'^$', FriendlyLinkListView.as_view(), name='web_friendly_links'),
)

__author__ = 'edison'
