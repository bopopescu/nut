from rest_framework import generics

from apps.core.models import  Selection_Article
from apps.api.serializers.articles import NestedSelectionArticleSerializer
from apps.api.permissions import  Admin_And_Editor_Only

class RFSlaListView(generics.ListCreateAPIView):
    permission_class=(Admin_And_Editor_Only,)

    queryset = Selection_Article.objects.all().order_by('-pub_time')
    serializer_class= NestedSelectionArticleSerializer
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by =  100

class RFSlaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (Admin_And_Editor_Only,)
    queryset = Selection_Article.objects.all()
    serializer_class = NestedSelectionArticleSerializer


