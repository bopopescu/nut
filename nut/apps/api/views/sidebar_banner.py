from  apps.core.models import Sidebar_Banner
from  apps.api.serializers.sidebar_banner import Sidebar_Banner_Serializer
from  rest_framework import generics
from  rest_framework import permissions


# use only the most simple permission class , only admin and editor get
# http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/

class Admin_And_Editor_Only(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_editor


#RF for restful ,
class RFSidebarBannerListView(generics.ListCreateAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Sidebar_Banner.objects.all()
    serializer_class = Sidebar_Banner_Serializer

class RFSidebarBannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Sidebar_Banner.objects.all()
    serializer_class = Sidebar_Banner_Serializer