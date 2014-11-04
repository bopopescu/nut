from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.media',
    url(r'^$', 'list', name='management_media_list'),
    url(r'^delete/$', 'delete', name='management_media_delete'),
    url(r'^upload/image/$', 'upload_image', name='management_upload_image'),
)

__author__ = 'edison'
