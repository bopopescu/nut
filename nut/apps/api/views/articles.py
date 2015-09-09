from rest_framework import generics
from rest_framework import filters
import django_filters

from apps.core.models import Article
from apps.api.serializers.articles import ArticleSerializer
from apps.api.permissions import  Admin_And_Editor_Only


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['publish']

class RFArticleListView(generics.ListCreateAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Article.objects.all().order_by('-updated_datetime')
    serializer_class = ArticleSerializer
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    filter_backends = (filters.DjangoFilterBackend,)
    filter_class =  ArticleFilter

class RFArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer