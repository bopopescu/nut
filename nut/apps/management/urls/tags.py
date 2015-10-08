from django.conf.urls import url, patterns
from apps.management.views.tags import TagListView, TagEntitiesView\
                                       ,EditTagFormView, ArticleTagListView\
                                       ,SwitchTopArticleTagView

urlpatterns = patterns(
    'apps.management.views.tags',
    # url(r'^$', 'list', name='management_tag_list'),
    url(r'^$', TagListView.as_view(), name='management_tag_list'),
    url(r'^article/(?P<tag_name>.*)/$', ArticleTagListView.as_view(), name='management_tag_articles'),
    url(r'^(?P<tag_id>\d+)/edit/$', EditTagFormView.as_view(), name='management_tag_edit'),
    url(r'^(?P<tag_id>\d+)/topArticleTag/$', SwitchTopArticleTagView.as_view(), name='management_tag_edit'),
    url(r'^(?P<tag_name>.*)/$', TagEntitiesView.as_view(), name='management_tag_entities'),
)

__author__ = 'edison'
