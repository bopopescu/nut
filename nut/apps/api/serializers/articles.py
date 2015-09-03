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
    status = serializers.SerializerMethodField()
    creator = NestingUserSerializer()
    class Meta:
        model = Article
        fields =  ('id','creator','status','title','selections','cover','publish','created_datetime','showcover','read_count','cover_url')

    def get_status(self, obj):
        return obj.get_publish_display()