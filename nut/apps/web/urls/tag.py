from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.web.views.tag',
    url(r'^(?P<tag_hash>\w+)/$', 'detail', name='web_tag_detail'),
)


__author__ = 'edison'
