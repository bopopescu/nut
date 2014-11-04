from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.article',
    url(r'^create/$', 'create', name="management_article_create"),
)

__author__ = 'edison'
