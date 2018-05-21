# coding=utf-8
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage

from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Entity, Entity_Like, Note_Poke, GKUser, PurchaseRecord
# from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
# from apps.core.models import Entity_Like
from apps.core.tasks import like_task, unlike_task, record_entity_view_task
from apps.mobile.models import Session_Key
# from apps.mobile.forms.search import EntitySearchForm
from apps.report.models import Report
from datetime import datetime
from apps.v4.models import APIEntity

from haystack.generic_views import SearchView
from apps.v4.forms.search import APIEntitySearchForm
from apps.v4.views import APIJsonView
from apps.core.views import JSONResponseMixin

from django.utils.log import getLogger

from utils.open_search_api import V3Api

log = getLogger('django')


from apps.v4.schema.users import UserSchema
from apps.v4.schema.entities import EntitySchema

users_schema    = UserSchema(many=True)
entities_schema = EntitySchema(many=True)


@check_sign
def entity_list(request):
    # log.info(request.GET)
    _timestamp = request.GET.get('timestamp', None)
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    else:
        _timestamp = datetime.now()


    log.info("time %s"% _timestamp )
    _sort_by = request.GET.get('sort', 'novus_time')
    _reverse = request.GET.get('reverse', '0')
    if _reverse == '0':
        _reverse = False
    else:
        _reverse = True

    _offset = int(request.GET.get('offset', '0'))
    _offset = _offset / 30 + 1
    _count = int(request.GET.get('count', '30'))


    _key = request.GET.get('session', None)
    # log.info("session "_key)
    entities = APIEntity.objects.new().filter(created_time__lt=_timestamp)[:30]

    try:
        _session = Session_Key.objects.get(session_key=_key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(entities))
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None

    res = []
    for row in entities:
        res.append(
            row.v4_toDict(user_like_list=el)
        )

    return SuccessJsonResponse(res)


class EntityDetailView(APIJsonView):

    def get_data(self, context):
        try:
            entity = APIEntity.objects.using('slave').get(pk=self.entity_id, status__gte=Entity.freeze)
        except APIEntity.DoesNotExist:
            return ErrorJsonResponse(status=404)

        el = None
        np = None
        if self.session:
            el = Entity_Like.objects.user_like_list(user=self.session.user, entity_list=[self.entity_id])
            np = Note_Poke.objects.user_poke_list(user=self.session.user,
                                                  note_list=list(entity.notes.values_list('id', flat=True)))

        likes = entity.likes.filter(user__is_active__gte=GKUser.active)

        rec = APIEntity.objects.guess(category_id=entity.category_id,
                                      count=9,
                                      exclude_id=entity.id)

        return {'entity': entity.v4_toDict(user_like_list=el),
                'note_list': [note.v4_toDict(user_note_pokes=np) for note in entity.notes.top_or_normal()],
                'like_user_list': [like.user.v3_toDict() for like in likes[:16]],
                'recommendation': entities_schema.dump(rec).data}

    def get(self, request, *args, **kwargs):
        self.entity_id  = kwargs.pop('entity_id', None)
        assert self.entity_id is not None

        _key = request.GET.get('session', None)

        try:
            self.session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist, e:
            log.info(e.message)
            self.session = None

        payload = {
            'entity_id': self.entity_id,
            'user_id': self.session.user_id if self.session else None,
            'device_uuid': request.GET.get('device_uuid', None)
        }

        record_entity_view_task.delay(**payload)

        return super(EntityDetailView, self).get(request, *args, **kwargs)

@csrf_exempt
@check_sign
def like_action(request, entity_id, target_status):
    if request.method == "POST":
        _key = request.POST.get('session', None)
        try:
            _session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)
        res = {
            'entity_id': entity_id,
        }

        if target_status == "1":
            like_task.delay(uid=_session.user_id, eid=entity_id)
            res['like_already'] = 1
        else:
            unlike_task.delay(uid=_session.user_id, eid=entity_id)
            res['like_already'] = 0
        return SuccessJsonResponse(res)

    return ErrorJsonResponse(status=400)


class EntityLikerView(APIJsonView):

    http_method_names = ['get']

    def get_data(self, context):
        liker = Entity_Like.objects.filter(entity=self.entity_id, user__is_active__gte=GKUser.active)

        paginator = Paginator(liker, 15)
        try:
            liker_list = paginator.page(self.page)
        except EmptyPage:
            return {
                'page': 1,
                'count': 0,
                'data': []
            }

        if self.session:
            users_schema.context['visitor'] = self.session.user
        return {
            'page': self.page,
            'count': liker.count(),
            'data': [users_schema.dump(row.user, many=False).data for row in liker_list.object_list]
        }

    def get(self, request, *args, **kwargs):
        self.entity_id = kwargs.pop('entity_id', None)
        assert self.entity_id is not None
        self.page = request.GET.get('page', 1)
        _key = request.GET.get('session', None)
        try:
            self.session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist, e:
            self.session = None
            log.info(e.message)

        return super(EntityLikerView, self).get(request, *args, **kwargs)


class GuessEntityView(APIJsonView):

    http_method_names = ['get']

    def get_data(self, context):

        # 推荐规则： 同一分类下，获取count*10个，然后其中随机取出count个
        entities = APIEntity.objects.guess(category_id=self.category_id,
                                           count=self.count,
                                           exclude_id=self.entity_id)

        result = [entity.v4_toDict() for entity in entities]
        return result

    def get(self, request, *args, **kwargs):
        self.category_id = request.GET.get('cid', None)
        self.entity_id = request.GET.get('eid', None)
        self.count = int(request.GET.get('count', '5'))

        return super(GuessEntityView, self).get(request, args, **kwargs)


class APIEntitySearchView(SearchView, JSONResponseMixin):
    form_class = APIEntitySearchForm
    http_method_names = ['get']

    def get_data(self, context):

        res = {
            'stat': {
                'all_count': context.count(),
                'like_count': 0,
            },
            'entity_list': []
        }

        el = None
        if self.visitor:
            _entity_id_list = map(lambda x: int(x.entity_id), context[self.offset:self.offset+self.count])
            el = Entity_Like.objects.user_like_list(user=self.visitor, entity_list=_entity_id_list)
        for row in context[self.offset:self.offset+self.count]:
            try:
                # row.object可能为None，此时跳过
                res['entity_list'].append(row.object.v3_toDict(user_like_list=el))
            except AttributeError:
                continue
        if el:
            res['stat']['like_count'] = len(el)

        return res

    def form_valid(self, form):
        self.queryset = form.search()
        return self.render_to_json_response(self.queryset)

    def form_invalid(self, form):
        return ErrorJsonResponse(status=400, data=form.errors)

    def get(self, request, *args, **kwargs):
        _key = request.GET.get('session', None)
        self.offset = int(request.GET.get('offset', '0'))
        self.count = int(request.GET.get('count', '30'))
        self.type = request.GET.get('type', None)
        try:
            _session = Session_Key.objects.get(session_key=_key)
            self.visitor = _session.user
        except Session_Key.DoesNotExist:
            self.visitor = None
        return super(APIEntitySearchView, self).get(request, *args, **kwargs)

    @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(APIEntitySearchView, self).dispatch(request, *args, **kwargs)


class APIEntitySearchView2(APIJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        keyword = self.request.GET.get('q')
        api = V3Api(endpoint=settings.OPEN_SEARCH_ENDPOINT, access_key=settings.OPEN_SEARCH_ACCESS_KEY_ID,
                    secret=settings.OPEN_SEARCH_ACCESS_KEY_SECRET, app_name=settings.OPEN_SEARCH_APP_NAME)
        params = {
            'query': u"config=start:0,hit:20&&query=default:'{}'".format(keyword),
        }

        data = api.search('entity', params)

        ids = [d['id'] for d in data['result']['items']]

        entities = Entity.objects.filter(pk__in=ids)

        result = {
            'stat': {
                'all_count': entities.count(),
                'like_count': 0,
            },
            'entity_list': [entity.v3_toDict() for entity in entities],
        }
        return result


@csrf_exempt
@check_sign
def report(request, entity_id):
    _key = request.POST.get('session')
    _comment = request.POST.get('comment', '')
    _type = request.POST.get('type', Report.sold_out)

    try:
        _session = Session_Key.objects.get(session_key=_key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=400)

    try:
        entity = APIEntity.objects.get(pk = entity_id)
    except APIEntity.DoesNotExist:
        return ErrorJsonResponse(status=404)

    r = Report(reporter=_session.user, type=_type, comment=_comment, content_object=entity)
    r.save()
    return SuccessJsonResponse({ "status" : 1 })


@csrf_exempt
def purchase(request, entity_id):
    if request.method == "POST":
        _key = request.POST.get('session', None)
        try:
            _session = Session_Key.objects.get(session_key=_key)
            user_id = _session.user_id
        except Session_Key.DoesNotExist:
            user_id = None

        # TODO: 改成异步处理
        device_uuid = request.POST.get('device_uuid', '')
        record = PurchaseRecord(user_id=user_id, entity_id=entity_id, device_uuid=device_uuid)
        record.save()

        return SuccessJsonResponse({'record_id': record.id})

    return ErrorJsonResponse(status=400)
