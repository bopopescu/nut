from rest_framework import serializers

from apps.seller.models import IndexPageMeta


class IndexPageMetaSerializer(serializers.ModelSerializer):
    writer_list = serializers.CharField()
    topic_tag_list = serializers.CharField()
    column_article_tag_list = serializers.CharField()

    def validate_writer_list(self, value):
        try:
            value = str(value).replace('\n', '')
            writer_list = value.split(',')
            return writer_list
        except:
            raise serializers.ValidationError('writer list field valid fail')

    def validate_topic_tag_list(self, value):
        try:
            value = str(value).replace('\n', '')
            the_list = value.split(',')
            return the_list
        except:
            raise serializers.ValidationError('writer list field valid fail')

    def validate_column_article_tag_list(self, value):
        try:
            value = str(value).replace('\n', '')
            the_list = value.split(',')
            return the_list
        except:
            raise serializers.ValidationError('writer list field valid fail')


    class Meta:
        model =IndexPageMeta
        fields = ('year', 'writer_list', 'topic_tag_list', 'column_article_tag_list')