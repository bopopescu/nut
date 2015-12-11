from django.conf.urls import  url, patterns
from apps.api.views.entity import WebEntityDetailView

urlpatterns = patterns(
    '',
    url(r'^(?P<pk>[0-9]+)/$', WebEntityDetailView.as_view() , name='restful_web_entity_detail'),

)