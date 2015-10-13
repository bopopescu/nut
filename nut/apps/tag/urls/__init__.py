from django.conf.urls import url, patterns
from apps.tag.views import TagListView, TagEntityView, TagArticleView, NewTagArticleView


urlpatterns = patterns(
    'apps.tag.views',
    url(r'^$', TagListView.as_view(), name='tag_list_url'),
    # url(r'^(?P<tag_name>.*)/$', TagEntityView.as_view(), name='tag_entities_url'),
    url(r'^(?P<tag_hash>\w+)/$', TagEntityView.as_view(), name='tag_entities_url'),
    url(r'^articles/(?P<tag_name>.*)/$', NewTagArticleView.as_view(), name='tag_articles_url'),


)

__author__ = 'xiejiaxin'
