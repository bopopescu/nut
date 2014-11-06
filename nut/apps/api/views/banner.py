from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework import permissions

from apps.core.models import Banner, Show_Banner
from apps.api.serializers.banner import BannerSerializer

from django.utils.log import getLogger

log = getLogger('django')


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAdminUser]

    @list_route(permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def show(self, request):
        inner_qs = Show_Banner.objects.all().values('banner_id')
        banners = Banner.objects.filter(pk__in=inner_qs)
        page = self.paginate_queryset(banners)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)



__author__ = 'edison'
