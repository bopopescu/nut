from rest_framework import generics

from apps.core.models import Article
from apps.api.serializers.articles import ArticleSerializer
from apps.api.permissions import  Admin_And_Editor_Only

class RFArticleListView(generics.ListCreateAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class RFArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer