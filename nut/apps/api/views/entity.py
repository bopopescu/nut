from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import detail_route, list_route
from rest_framework import generics
from rest_framework import permissions
#
from apps.core.models import Entity
from apps.api.serializers.entity import EntitySerializer, WebEntitySerializer
# from apps.api.perm import IsOwnerOrReadOnly


from django.utils.log import getLogger

log = getLogger('django')



class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.filter(status__gt=Entity.remove)
    serializer_class = EntitySerializer
    # permission_classes = ( IsOwnerOrReadOnly, permissions.IsAdminUser, )
    # permission_classes = ( IsOwnerOrReadOnly, )


class SelectionViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.filter(status=Entity.selection)
    serializer_class = EntitySerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly, )


class WebEntityDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WebEntitySerializer
    queryset = Entity.objects.active()




__author__ = 'edison7500'
