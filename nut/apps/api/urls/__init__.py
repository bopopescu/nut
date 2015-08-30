from django.conf.urls import url, include, patterns
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from apps.api.views import user, entity, banner


router = routers.DefaultRouter()
router.register(r'user', user.UserViewSet),
router.register(r'entities', entity.EntityViewSet),
# router.register(r'selection', entity.SelectionViewSet),
router.register(r'banner', banner.BannerViewSet),


selection_list = entity.SelectionViewSet.as_view({
    'get': 'list',
})


selection_detail = entity.SelectionViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    # 'patch': 'partial_update',
    # 'delete': 'destroy',
})

#
urlpatterns = patterns(
    'apps.api.views',
    # url(r'^entities/', include('apps.api.urls.entities')),
    url(r'^', include(router.urls)),
    # url(r'^feed/', include('apps.mobile.urls.feed')),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
)

# urlpatterns += patterns(
#     'apps.api.views',
#     url(r'^feed/', include('apps.mobile.urls.feed')),
# )

# urlpatterns += format_suffix_patterns([
#     # url(r'^$',)
# ])



# urlpatterns += format_suffix_patterns([
#     # url(r'^$', api_root),
#     url(r'^selection/$', selection_list, name='selection-list'),
#     url(r'^selection/(?P<pk>[0-9]+)/$', selection_detail, name='selection-detail'),
# ])



# urlpatterns += patterns(
#     'apps.api.views',
#
# )



__author__ = 'edison7500'
