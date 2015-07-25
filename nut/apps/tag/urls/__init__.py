from django.conf.urls import url, patterns
from apps.tag.views import TagListView, TagEntityView


urlpatterns = patterns(
    'apps.tag.views',
    url(r'^$', TagListView.as_view(), name='tag_list_url'),
    url(r'^(?P<tag_name>\w+)/$', TagEntityView.as_view(), name='tag_entities_url'),
    url(r'^articles/(?P<tag_name>\w+)/$', TagEntityView.as_view(), name='tag_entities_url'),
)

__author__ = 'xiejiaxin'
