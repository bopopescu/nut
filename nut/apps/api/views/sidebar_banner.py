from  apps.core.models import Sidebar_Banner
from  apps.api.serializers.sidebar_banner import Sidebar_Banner_Serializer
from  rest_framework import generics

from apps.api.permissions import  Admin_And_Editor_Only
# use only the most simple permission class , only admin and editor get
# http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/



#RF for restful ,
class RFSidebarBannerListView(generics.ListCreateAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Sidebar_Banner.objects.all()
    serializer_class = Sidebar_Banner_Serializer

class RFSidebarBannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Sidebar_Banner.objects.all()
    serializer_class = Sidebar_Banner_Serializer