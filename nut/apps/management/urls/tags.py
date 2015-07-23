from django.conf.urls import url, patterns
from apps.management.views.tags import TagListView, TagEntitiesView, EditTagFormView, ArticleTagListView

urlpatterns = patterns(
    'apps.management.views.tags',
    # url(r'^$', 'list', name='management_tag_list'),
    url(r'^$', TagListView.as_view(), name='management_tag_list'),
    url(r'^(?P<tag_name>(\w|-)+)/$', TagEntitiesView.as_view(), name='management_tag_entities'),
    url(r'^article/(?P<tag_name>(\w|\-)+)/$', ArticleTagListView.as_view(), name='management_tag_articles'),
    url(r'^(?P<tag_id>\d+)/edit/$', EditTagFormView.as_view(), name='management_tag_edit'),
)

__author__ = 'edison'
