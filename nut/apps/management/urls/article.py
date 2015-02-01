from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.article',
    url(r'^$', 'list', name="management_article_list"),
    url(r'^create/$', 'create', name="management_article_create"),
    url(r'^(?P<article_id>\d+)/edit/$', 'edit', name='management_article_edit'),
    url(r'^(?P<article_id>\d+)/cover/upload/$', 'upload_cover', name='management_article_cover_upload'),
    url(r'^(?P<article_id>\d+)/preview/$', 'preview', name='management_article_preview'),
)

__author__ = 'edison'
