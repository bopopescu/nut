from rest_framework import serializers


from apps.core.models import Article, Selection_Article

from apps.api.serializers.user import NestingUserSerializer

# the following serializer is for ArticleSerializer nested use only
class NestedSelectionArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection_Article
        fields = ('is_published','create_time','pub_time', )


class ArticleSerializer(serializers.ModelSerializer):
    selections = NestedSelectionArticleSerializer(many=True)
    creator = NestingUserSerializer()
    class Meta:
        model = Article
        fields =  ('id','creator','title','selections','cover','published','created_datetime','showcover','read_count','cover_url')

