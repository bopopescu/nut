from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.article',
    url(r'^$', 'list', name="management_article_list"),
    url(r'^create/$', 'create', name="management_article_create"),
    url(r'^(?P<article_id>\d+)/edit/$', 'edit', name='management_article_edit'),
)

__author__ = 'edison'
