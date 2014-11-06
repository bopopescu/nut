from django.conf.urls import url, include, patterns
from rest_framework import routers

from apps.api.views import user, entity, banner


router = routers.DefaultRouter()
router.register(r'user', user.UserViewSet),
router.register(r'entity', entity.EntityViewSet),
router.register(r'banner', banner.BannerViewSet),



urlpatterns = patterns(
    'apps.api.views',
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
    # url()
)



__author__ = 'edison7500'
