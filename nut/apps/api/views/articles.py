from rest_framework import generics

from apps.core.models import Article
from apps.api.serializers.articles import ArticleSerializer
from apps.api.permissions import  Admin_And_Editor_Only

class RFArticleListView(generics.ListCreateAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class RFArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (Admin_And_Editor_Only,)

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer