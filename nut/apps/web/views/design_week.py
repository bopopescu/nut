from django.http import HttpResponseRedirect
from haystack.query import SearchQuerySet
from rest_framework import serializers
from rest_framework.pagination import BasePaginationSerializer
from rest_framework.response import Response

from apps.core.models import Selection_Entity, GKUser, Entity, Buy_Link
from rest_framework import viewsets

shop_link_list = ['http://shop62876401.taobao.com', 'http://shop106513024.taobao.com', 'http://shop34059034.taobao.com',
                  'http://shop59335680.taobao.com', 'http://shop101345951.taobao.com', 'http://shop63619704.taobao.com',
                  'http://shop33814870.taobao.com', 'http://shop34018187.taobao.com', 'http://shop71703982.taobao.com',
                  'http://shop100303622.taobao.com', 'http://shop103766985.taobao.com', 'http://shop108247399.taobao.com',
                  'http://shop65626903.taobao.com', 'http://shop104013601.taobao.com', 'http://shop108981965.taobao.com',
                  'http://shop34810568.taobao.com', 'http://shop115072463.taobao.com', 'http://shop124545542.taobao.com',
                  'http://shop101156075.taobao.com', 'http://shop144067355.taobao.com', 'http://shop35320374.taobao.com',
                  'http://shop104734695.taobao.com', 'http://shop117129254.taobao.com', 'http://shop36273178.taobao.com',
                  'http://shop64427786.taobao.com', 'http://shop108552880.taobao.com', 'http://shop105219577.taobao.com',
                  'http://shop144097624.taobao.com', 'http://shop59753514.taobao.com', 'http://shop114039340.taobao.com',
                  'http://shop104324573.taobao.com', 'http://shop112908081.taobao.com', 'http://shop67697225.taobao.com',
                  'http://shop67735063.taobao.com', 'http://shop111642953.taobao.com', 'http://shop110909976.taobao.com',
                  'http://shop104296744.taobao.com', 'http://shop36409483.taobao.com', 'http://shop64675842.taobao.com',
                  'http://shop72022510.taobao.com', 'http://shop104624824.taobao.com', 'http://shop73267382.taobao.com',
                  'http://shop115168895.taobao.com', 'http://shop107880160.taobao.com', 'http://shop73213611.taobao.com',
                  'http://shop35367109.taobao.com', 'http://shop68623508.taobao.com', 'http://shop67612925.taobao.com',
                  'http://shop33706346.taobao.com', 'http://shop64485008.taobao.com', 'http://shop60588691.taobao.com',
                  'http://shop112152154.taobao.com', 'http://shop103089473.taobao.com', 'http://shop100414463.taobao.com',
                  'http://shop112879610.taobao.com', 'http://shop63445215.taobao.com', 'http://shop102999862.taobao.com',
                  'http://shop68444170.taobao.com', 'http://shop69630264.taobao.com', 'http://shop72035370.taobao.com',
                  'http://shop69723005.taobao.com', 'http://shop106967109.taobao.com', 'http://shop108052533.taobao.com',
                  'http://shop67761298.taobao.com', 'http://shop116338709.taobao.com', 'http://shop105990842.taobao.com',
                  'http://shop33409147.taobao.com', 'http://shop121993332.taobao.com', 'http://shop108070058.taobao.com',
                  'http://shop106015025.taobao.com', 'http://shop34147835.taobao.com', 'http://shop136886826.taobao.com',
                  'http://shop120153891.taobao.com', 'http://shop104430735.taobao.com', 'http://shop66194969.taobao.com',
                  'http://shop60679441.taobao.com', 'http://shop117034379.taobao.com', 'http://shop109855521.taobao.com',
                  'http://shop135547259.taobao.com', 'http://shop107514636.taobao.com', 'http://shop62028563.taobao.com',
                  'http://shop110079009.taobao.com', 'http://shop108522753.taobao.com', 'http://shop114683150.taobao.com',
                  'http://shop107307345.taobao.com', 'http://shop107765987.taobao.com', 'http://shop113913001.taobao.com',
                  'http://shop68916276.taobao.com', 'http://shop103528419.taobao.com', 'http://shop120321737.taobao.com',
                  'http://shop70539661.taobao.com', 'http://shop58730264.taobao.com', 'http://shop106240611.taobao.com',
                  'http://shop104500518.taobao.com', 'http://shop69165605.taobao.com', 'http://shop73060578.taobao.com',
                  'http://shop64043278.taobao.com', 'http://shop63694145.taobao.com', 'http://shop34694733.taobao.com',
                  'http://shop71036919.taobao.com', 'http://shop118104581.taobao.com', 'http://shop33439744.taobao.com',
                  'http://shop68351937.taobao.com', 'http://shop90149.taobao.com', 'http://shop61739784.taobao.com',
                  'http://shop36933532.taobao.com', 'http://shop115743542.taobao.com', 'http://shop70131763.taobao.com',
                  'http://shop101135924.taobao.com', 'http://shop100540114.taobao.com', 'http://shop111481369.taobao.com',
                  'http://shop109718704.taobao.com', 'http://shop102774711.taobao.com', 'http://shop111004977.taobao.com',
                  'http://shop115192784.taobao.com', 'http://shop123247088.taobao.com', 'http://shop115093764.taobao.com',
                  'http://shop115862174.taobao.com', 'http://shop103709663.taobao.com', 'http://shop71212486.taobao.com',
                  'http://shop105613272.taobao.com', 'http://shop106763520.taobao.com', 'http://shop143147160.taobao.com',
                  'http://shop112842622.taobao.com', 'http://shop102850013.taobao.com', 'http://shop111653948.taobao.com', 'http://shop111292426.taobao.com', 'http://shop112479787.taobao.com', 'http://shop105301969.taobao.com', 'http://shop73147035.taobao.com', 'http://shop108528222.taobao.com', 'http://shop108127530.taobao.com', 'http://shop68491334.taobao.com', 'http://shop105660753.taobao.com', 'http://shop63302399.taobao.com', 'http://shop103407242.taobao.com', 'http://shop115695999.taobao.com', 'http://shop118252506.taobao.com', 'http://shop62831944.taobao.com', 'http://shop62193774.taobao.com', 'http://shop106501632.taobao.com', 'http://shop112664193.taobao.com', 'http://shop102911018.taobao.com', 'http://shop145412620.taobao.com', 'http://shop112831063.taobao.com', 'http://shop36472211.taobao.com', 'http://shop67725366.taobao.com', 'http://shop112830182.taobao.com', 'http://shop108148339.taobao.com', 'http://shop111396427.taobao.com', 'http://shop113239522.taobao.com', 'http://shop111457438.taobao.com', 'http://shop116017462.taobao.com', 'http://shop109584705.taobao.com', 'http://shop109763080.taobao.com', 'http://shop104438493.taobao.com', 'http://shop106187424.taobao.com', 'http://shop121118516.taobao.com', 'http://shop65468393.taobao.com', 'http://shop71164775.taobao.com', 'http://shop110251771.taobao.com', 'http://shop115483100.taobao.com', 'http://shop126955041.taobao.com', 'http://shop105890659.taobao.com', 'http://shop34214433.taobao.com', 'http://shop100968753.taobao.com', 'http://shop33468699.taobao.com', 'http://shop72581140.taobao.com', 'http://shop59161058.taobao.com', 'http://shop117703430.taobao.com', 'http://shop64122700.taobao.com', 'http://shop68099128.taobao.com', 'http://shop60897763.taobao.com', 'http://shop100897079.taobao.com',]



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
        self.permission_classes = ()
        self.page_kwarg = 'page_offset'
        self.paginate_by_param = 'page_size'
        self.serializer_class = DesignWeekSerializer
        self.queryset = self.get_queryset()

    def list(self, request, *args, **kwargs):
        if request.query_params == {}:
            return HttpResponseRedirect(request.path + "?page_size=30&page_offset=1")
        instance = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        # auth_seller = GKUser.objects.authorized_seller()
        # Selection_Entity.objects.filter(entity__user__in=list(auth_seller)).order_by('pub_time')
        # entities = Entity.objects.filter(user__in=list(auth_seller), status=1)
        entities = Entity.objects.filter(buy_links__shop_link__in=shop_link_list, status=1)
        # obj = SearchQuerySet().models(Entity).filter(is_in_selection=True, user__in=auth_seller).order_by('-enter_selection_time')
        # entity_ids = obj.values_list('entity_id', flat=True)
        # qs = Entity.objects.filter(id__in=entity_ids)
        return entities


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









