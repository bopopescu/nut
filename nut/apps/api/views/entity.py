from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework import permissions

from apps.core.models import Entity
from apps.api.serializers.entity import EntitySerializer

from django.utils.log import getLogger

log = getLogger('django')



class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [permissions.IsAdminUser]
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          # IsOwnerOrReadOnly,)

    # @detail_route(methods=['post'])
    # def

    # def list(self, request, *args, **kwargs):

        # return


    @list_route(permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def selection(self, request):
        # log.info(request)
        selection_entity = Entity.objects.filter(status=Entity.selection)
        page = self.paginate_queryset(selection_entity)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)



__author__ = 'edison7500'
