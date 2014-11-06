from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from apps.core.models import Entity
from apps.api.serializers.entity import EntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer

    @list_route(methods=['get'])
    def recent_users(self, request):
        recent_entity = Entity.objects.all()
        page = self.paginate_queryset(recent_entity)
        serializer = self.get_pagination_serializer(page)
        return  Response(serializer)

__author__ = 'edison7500'
