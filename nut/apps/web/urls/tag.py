from django.conf.urls import url, patterns
from apps.web.views.tag import TagHashView,TagArticleList

urlpatterns = patterns(
    'apps.web.views.tag',
    # url(r'^(?P<hash>\w+)/$', 'detail', name='web_tag_detail'),
    url(r'^(?P<hash>\w+)/$', TagHashView.as_view(), name='web_tag_detail'),
)

__author__ = 'edison'
