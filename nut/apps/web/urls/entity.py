from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.entity',
    url(r'^(?P<entity_hash>\w+)/$', 'entity_detail', name='web_entity_detail')
)

__author__ = 'edison'
