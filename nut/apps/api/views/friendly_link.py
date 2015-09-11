from apps.core.models import Friendly_Link
from apps.api.serializers.friendly_link import Friendly_Link_Serializer

from rest_framework import generics
from apps.api.permissions import Admin_And_Editor_Only

class RFFriendlyLinkListView(generics.ListCreateAPIView):
    permission_classes = (Admin_And_Editor_Only,)
    queryset =  Friendly_Link.objects.all()
    serializer_class = Friendly_Link_Serializer

class RFFriendlyLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (Admin_And_Editor_Only)
    queryset = Friendly_Link.objects.all()
    serializer_class = Friendly_Link_Serializer

