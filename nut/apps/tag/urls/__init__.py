from django.conf.urls import url, patterns
from apps.tag.views import TagListView, TagEntityView


urlpatterns = patterns(
    'apps.tag.views',
    url(r'^$', TagEntityView.as_view(), name='tag_list_url'),

)

__author__ = 'xiejiaxin'
