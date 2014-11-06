from django.conf.urls import url, include, patterns
from rest_framework import routers

from apps.api.views import user, entity


router = routers.DefaultRouter()
router.register(r'user', user.UserViewSet),
router.register(r'entity', entity.EntityViewSet),

urlpatterns = patterns(
    'apps.api.views',
    url(r'^', include(router.urls)),
    # url()
)



__author__ = 'edison7500'
