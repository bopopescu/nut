from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
# from rest_framework import permissions

from apps.core.models import Entity
from apps.api.serializers.entity import EntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          # IsOwnerOrReadOnly,)

    # @detail_route(methods=['post'])
    # def


    @list_route()
    def selection_entity(self, request):
        selection_entity = Entity.objects.filter(status=Entity.selection)
        page = self.paginate_queryset(selection_entity)
        serializer = self.get_pagination_serializer(page)
        return  Response(serializer)

__author__ = 'edison7500'
