from haystack.query import SearchQuerySet
from rest_framework import serializers
from rest_framework.pagination import BasePaginationSerializer

from apps.core.models import Selection_Entity, GKUser, Entity
from rest_framework import viewsets



class DesignWeekSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='design_week_url', read_only=True)
    liked = serializers.IntegerField(source='like_count', read_only=True)
    image = serializers.CharField(source='chief_image', read_only=True)
    price = serializers.IntegerField(read_only=True)
    class Meta:
        model = Entity
        fields = ('title', 'price', 'image', 'url', 'liked')

class DesignWeekViewSet(viewsets.ReadOnlyModelViewSet):

    def __init__(self, *args, **kwargs):
        super(DesignWeekViewSet, self).__init__(**kwargs)
        self.page_kwarg = 'page_offset'
        self.paginate_by_param = 'page_size'
        self.serializer_class = DesignWeekSerializer
        self.queryset = self.get_queryset()

    def get_queryset(self):
        auth_seller = GKUser.objects.authorized_seller()
        obj = SearchQuerySet().models(Entity).filter(is_in_selection=True, user__in=auth_seller).order_by('-enter_selection_time')
        entity_ids = obj.values_list('entity_id', flat=True)
        qs = Entity.objects.filter(id__in=entity_ids)
        return qs


    def get_pagination_serializer(self, page):
        class SerializerClass(NewPaginationSerializer):
            class Meta:
                object_serializer_class = self.get_serializer_class()
        pagination_serializer_class = SerializerClass
        context = self.get_serializer_context()
        return pagination_serializer_class(instance=page, context=context)


class DesignWeekPaginationSerializer(BasePaginationSerializer):

    total_count = serializers.ReadOnlyField(source='paginator.count')
    page_size = serializers.SerializerMethodField('get_pagesize')
    page_offset = serializers.SerializerMethodField('get_pageoffset')

    def get_pagesize(self, page):
        return int(self.context['request'].query_params.get('page_size'))

    def get_pageoffset(self, page):
        return int(self.context['request'].query_params.get('page_offset'))



class NewPaginationSerializer(DesignWeekPaginationSerializer):

    def __init__(self, *args, **kwargs):
        self.results_field = 'data'
        super(NewPaginationSerializer, self).__init__(*args, **kwargs)









