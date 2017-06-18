# coding=utf-8
from django.views.decorators.csrf import csrf_exempt

from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Entity, Entity_Like, Note_Poke, PurchaseRecord
from apps.core.tasks import like_task, unlike_task
from apps.mobile.models import Session_Key
from apps.report.models import Report
from datetime import datetime

from apps.core.views import JSONResponseMixin
from apps.mobile.forms.search import APIEntitySearchForm
from haystack.generic_views import SearchView


from django.utils.log import getLogger
log = getLogger('django')


@check_sign
def entity_list(request):
    log.info(request.GET)
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
    entities = Entity.objects.new().filter(created_time__lt=_timestamp)[:30]

    try:
        _session = Session_Key.objects.get(session_key=_key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(entities))
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None

    res = []
    for row in entities:
        res.append(
            row.v3_toDict(user_like_list=el)
        )

    return SuccessJsonResponse(res)


@check_sign
def detail(request, entity_id):
    # log.info("v3v3v3v3vv3")
    _key = request.GET.get('session', None)
    # log.info("session "_key)
    try:
        entity = Entity.objects.get(pk=entity_id, status__gte=Entity.freeze)
    except Entity.DoesNotExist:
        return ErrorJsonResponse(status=404)

    try:
        _session = Session_Key.objects.get(session_key=_key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=[entity_id])
        np = Note_Poke.objects.user_poke_list(user=_session.user,  note_list=list(entity.notes.values_list('id', flat=True)))
        # np = Note_Poke.objects.filter(user=_session.user, note_id__in=list(entity.notes.values_list('id', flat=True))).values_list('note_id', flat=True)
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None
        np = None

    # log.info(np)
    # log.info(el)
    res = dict()

    res['entity'] = entity.v3_toDict(user_like_list=el)
    res['note_list'] = []


    for note in entity.notes.top_or_normal():
        res['note_list'].append(
            note.v3_toDict(user_note_pokes=np)
        )

    res['like_user_list'] = []
    for liker in entity.likes.all()[0:10]:
        res['like_user_list'].append(
            liker.user.v3_toDict()
        )

    return SuccessJsonResponse(res)


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
            # try:
            #     Entity_Like.objects.get(user_id=_session.user_id, entity_id=entity_id)
            # except Entity_Like.DoesNotExist:
            #     Entity_Like.objects.create(
            #         user_id = _session.user_id,
            #         entity_id = entity_id
            #     )
            res['like_already'] = 1
        else:
            # try:
            #     el = Entity_Like.objects.get(user_id=_session.user_id, entity_id=entity_id)
            #     el.delete()
            # except Entity_Like.DoesNotExist, e:
            #     log.info("info %s", e.message)
            unlike_task.delay(uid=_session.user_id, eid=entity_id)
            res['like_already'] = 0
        return SuccessJsonResponse(res)

    return ErrorJsonResponse(status=400)


@check_sign
def guess(request):

    res = []

    _category_id = request.GET.get('cid', None)
    _count = int(request.GET.get('count', '5'))

    entities = Entity.objects.guess(category_id=_category_id, count=_count)

    for entity in entities:
        res.append(entity.v3_toDict())

    return SuccessJsonResponse(res)

class APIEntitySearchView(SearchView, JSONResponseMixin):
    form_class = APIEntitySearchForm
    http_method_names = ['get']

    def get_data(self, context):
        # print context
        res = {
            'stat' : {
                'all_count' : context.count(),
                'like_count' : 0,
            },
            'entity_list' : []
        }

        el = None
        if self.visitor:
            _entity_id_list = map(lambda x : int(x.object.id), context[self.offset:self.offset+self.count])
            el = Entity_Like.objects.user_like_list(user = self.visitor, entity_list=_entity_id_list)
            # log.info(el)
        for row in context[self.offset:self.offset+self.count]:
            res['entity_list'].append(
                row.object.v3_toDict(user_like_list=el)
            )
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

    def dispatch(self, request, *args, **kwargs):
        return super(APIEntitySearchView, self).dispatch(request, *args, **kwargs)


@csrf_exempt
@check_sign
def report(request, entity_id):
    _key = request.POST.get('session')
    _comment = request.POST.get('comment', '')
    try:
        _session = Session_Key.objects.get(session_key=_key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=400)

    try:
        entity = Entity.objects.get(pk = entity_id)
    except Entity.DoesNotExist:
        return ErrorJsonResponse(status=404)

    r = Report(reporter=_session.user, type=Report.sold_out, comment=_comment, content_object=entity)
    r.save()
    return SuccessJsonResponse({ "status" : 1 })


@csrf_exempt
@check_sign
def purchase_action(request, entity_id):
    if request.method == "POST":
        _key = request.POST.get('session', None)
        try:
            _session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)
        res = {
            'entity_id': entity_id,
        }

        # TODO: 改成异步处理
        PurchaseRecord.objects.create(user_id=_session.user_id, entity_id=entity_id)

        return SuccessJsonResponse(res)

    return ErrorJsonResponse(status=400)
