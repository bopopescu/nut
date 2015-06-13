from django.conf.urls import url, patterns
from apps.management.views.article import SelectionArticleList


urlpatterns = patterns(
    'apps.management.views.article',
    url(r'^$', 'list', name="management_article_list"),
    url(r'^create/$', 'create', name="management_article_create"),
    url(r'^(?P<article_id>\d+)/edit/$', 'edit', name='management_article_edit'),
    url(r'^(?P<article_id>\d+)/cover/upload/$', 'upload_cover', name='management_article_cover_upload'),
    url(r'^(?P<article_id>\d+)/preview/$', 'preview', name='management_article_preview'),
    # by An , handle selection Article
    url(r'^selection/', SelectionArticleList.as_view(), name='management_selection_article_list')
)

__author__ = 'edison'
