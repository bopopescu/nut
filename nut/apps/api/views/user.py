from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from apps.core.models import GKUser
from apps.api.serializers.user import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = GKUser.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['get'])
    def recent_users(self, request):
        recent_users = GKUser.objects.filter(is_active=GKUser.active).order('-last_login')
        page = self.paginate_queryset(recent_users)
        serializer = self.get_pagination_serializer(page)
        return  Response(serializer)

__author__ = 'edison7500'
