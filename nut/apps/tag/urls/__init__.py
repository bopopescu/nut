from django.conf.urls import url, patterns
from apps.tag.views import TagListView, TagEntitiesByHashView, \
                            TagArticleView, TagEntityView, \
                            ArticleTagView


urlpatterns = patterns(
    'apps.tag.views',
    url(r'^$', TagListView.as_view(), name='tag_list_url'),
    # url(r'^(?P<tag_name>.*)/$', TagEntityView.as_view(), name='tag_entities_url'),
    # url(r'^articles/(?P<tag_name>.*)/$', TagArticleView.as_view(), name='tag_articles_url'),
    url(r'^articles/(?P<tag_name>.*)/$', ArticleTagView.as_view(), name='tag_articles_url'),
    url(r'^name/(?P<tag_name>.*)/$', TagEntityView.as_view(), name='tag_name_entities_url'),
    url(r'^(?P<tag_hash>\w+)/$', TagEntitiesByHashView.as_view(), name='tag_entities_url'),
)

__author__ = 'xiejiaxin'
