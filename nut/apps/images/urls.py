from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.images.views',
    url(r'^(?P<size>\d+)/(?P<file_name>.*)$', 'images', name='web_images'),
    url(r'^(?P<file_name>.*)$', 'images', name='web_images'),

)



__author__ = 'edison'
