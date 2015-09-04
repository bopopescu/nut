from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import GKUser, Entity_Like, Note, User_Follow
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger

from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.mobile.forms.user import MobileUserProfileForm
from apps.mobile.forms.search import UserSearchForm

from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
from django.utils.log import getLogger
from datetime import datetime
import time

from apps.tag.models import Content_Tags

from apps.core.views import JSONResponseMixin
from apps.v4.forms.search import APIUserSearchForm
from haystack.generic_views import SearchView

log = getLogger('django')


@csrf_exempt
@check_sign
def update(request):
    if request.method == "POST":
        # log.info(request.POST)
        # log.info(request.FILES)
        _key = request.POST.get('session', None)
        try:
            _session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)

        _forms = MobileUserProfileForm(user=_session.user, data=request.POST, files=request.FILES)
        if _forms.is_valid():
            res = _forms.save()
            return SuccessJsonResponse(res)
    return ErrorJsonResponse(status=400)


@check_sign
def detail(request, user_id):

    _key = request.GET.get('session')

    try:
        _session = Session_Key.objects.get(session_key=_key)
        visitor = _session.user
    except Session_Key.DoesNotExist:
        visitor = None

    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        raise ErrorJsonResponse(status=404)

    _last_like = Entity_Like.objects.filter(user=_user).last()
    _last_note = Note.objects.filter(user=_user).last()

    res = dict()
    res['user'] = _user.v3_toDict(visitor)
    if _last_like:
        res['last_like'] = _last_like.entity.v3_toDict()
    if _last_note:
        res['last_note'] = _last_note.v3_toDict()

    return SuccessJsonResponse(res)


@check_sign
def tag_list(request, user_id):

    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)


    res = {}
    res['user'] = _user.v3_toDict()
    # res['tags'] = Entity_Tag.objects.user_tags(user=_user.pk)
    res['tags'] = res['tags'] = Content_Tags.objects.user_tags(user=_user.pk)
    return SuccessJsonResponse(res)


@check_sign
def tag_detail(request, user_id, tag):
    _key = request.GET.get('session')

    try:
        user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    tags = Content_Tags.objects.filter(creator_id=user_id, tag__name=tag, target_content_type_id=24)
    try:
        _session = Session_Key.objects.get(session_key = _key)
        _eid_list = Note.objects.filter(pk__in=tags.values_list('target_object_id', flat=True)).values_list('entity_id', flat=True)
        # eid_list = Note.objects.filter(pk__in=)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(_eid_list))
    except Session_Key.DoesNotExist:
        el = None

    res = dict()
    res['user'] = user.v3_toDict()
    res['entity_list'] = []
    for row in tags:
        entity = row.target.entity
        res['entity_list'].append(entity.v3_toDict(user_like_list=el))

    return SuccessJsonResponse(res)


@check_sign
def entity_like(request, user_id):
    # log.info(request.GET)
    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    _key = request.GET.get('session')


    _timestamp = request.GET.get('timestamp', datetime.now())
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    else:
        _timestamp = datetime.now()
    # _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))
    log.info(_timestamp)
    # _offset = _offset / _count + 1

    res = {}
    # res['timestamp'] = time.mktime(_timestamp.timetuple())
    res['entity_list'] = []

    entities = Entity_Like.objects.filter(user=_user, created_time__lt=_timestamp)[:_count]
    last = len(entities) -1
    res['timestamp'] = time.mktime(entities[last].created_time.timetuple())


    try:
        _session = Session_Key.objects.get(session_key=_key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(entities.values_list('entity_id', flat=True)))
    except Session_Key.DoesNotExist:
        el = None

    for like in entities:
        try:
            e = like.entity.v3_toDict(el)
        except Exception, e:
            log.error("Error: %s" % e.message)
            continue
        res['entity_list'].append(
            e
        )

    return SuccessJsonResponse(res)


@check_sign
def entity_note(request, user_id):
    log.info(request.GET)

    try:
        _user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))

    _offset = _offset / _count + 1

    _timestamp = request.GET.get('timestamp', datetime.now())
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))

    notes = Note.objects.filter(user=_user, post_time__lt=_timestamp).exclude(status=-1).order_by('-post_time')[:_count]
    res = []
    for note in notes:
        log.info(note)
        res.append({
            'note': note.v3_toDict(),
            'entity': note.entity.v3_toDict(),
        })

    return SuccessJsonResponse(res)


@check_sign
def following_list(request, user_id):

    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))
    if _offset > 0 and _offset < 30:
        return ErrorJsonResponse(status=404)
    _offset = _offset / _count + 1

    _key = request.GET.get('session')

    try:
        _session = Session_Key.objects.get(session_key=_key)
        visitor = _session.user
    except Session_Key.DoesNotExist:
        visitor = None

    try:
        _user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    followings_list = _user.followings.all()

    paginator = Paginator(followings_list, _count)

    try:
        _followings = paginator.page(_offset)
    # except PageNotAnInteger:
    #     _followings = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)

    res = []
    for user in _followings.object_list:
        res.append(
            user.followee.v3_toDict(visitor=visitor)
        )

    return SuccessJsonResponse(res)


@check_sign
def fans_list(request, user_id):

    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))
    if _offset > 0 and _offset < 30:
        return ErrorJsonResponse(status=404)
    _offset = _offset / _count + 1

    _key = request.GET.get('session')
    try:
        _session = Session_Key.objects.get(session_key=_key)
        visitor = _session.user
    except Session_Key.DoesNotExist:
        visitor = None
    try:
        _user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    fans_list = _user.fans.all()
    paginator = Paginator(fans_list, 30)

    try:
        _fans = paginator.page(_offset)
    # except PageNotAnInteger:
    #     _fans = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)


    res = []
    for user in _fans.object_list:
        res.append(
            user.follower.v3_toDict(visitor=visitor)
        )
    return SuccessJsonResponse(res)


@csrf_exempt
@check_sign
def follow_action(request, user_id, target_status):

    if request.method == "GET":
        return ErrorJsonResponse(status=400)

    log.info(request.POST)

    _key = request.POST.get('session')

    try:
        _session = Session_Key.objects.get(session_key = _key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=400)

    res = {
        'user_id':user_id
    }

    if target_status == '1':
        try:
            uf = User_Follow.objects.get(
                follower = _session.user,
                followee_id = user_id,
            )
            return ErrorJsonResponse(status=400)
        except User_Follow.DoesNotExist, e:
            uf = User_Follow(
                follower = _session.user,
                followee_id = user_id,
            )
            uf.save()
            log.info(_session.user.following_list)
            if uf.followee_id in _session.user.fans_list:
                res['relation'] = 3
            else:
                res['relation'] = 1
    else:
        try:
            uf = User_Follow.objects.get(
                follower = _session.user,
                followee_id = user_id,
            )
            uf.delete()
            # if user_id in _session.user.following_list:
            res['relation'] = 0
        except User_Follow.DoesNotExist, e:
            return ErrorJsonResponse(status=400)
    return SuccessJsonResponse(res)


class APIUserSearchView(SearchView, JSONResponseMixin):
    form_class = APIUserSearchForm
    http_method_names = ['get']

    def get_data(self, context):
        res = []
        for row in context[self.offset: self.offset+self.count]:
            res.append(
                row.object.v3_toDict(visitor=self.visitor)
            )
        return res

    def form_valid(self, form):
        self.queryset = form.search()
        return self.render_to_json_response(self.queryset)

    def form_invalid(self, form):
        return ErrorJsonResponse(status=400)

    def get(self, request, *args, **kwargs):
        _key = request.GET.get('session', None)
        self.offset = int(request.GET.get('offset', '0'))
        self.count = int(request.GET.get('count', '30'))
        try:
            _session = Session_Key.objects.get(session_key=_key)
            self.visitor = _session.user
        except Session_Key.DoesNotExist:
            self.visitor = None
        return super(APIUserSearchView, self).get(request, *args, **kwargs)

    @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(APIUserSearchView, self).dispatch(request, *args, **kwargs)

# @check_sign
# def search(request):
#     _offset = int(request.GET.get('offset', '0'))
#     _count = int(request.GET.get('count', '30'))
#
#     if _offset > 0 and _offset < 30:
#         return ErrorJsonResponse(status=404)
#
#     _offset = _offset / _count + 1
#
#     _forms = UserSearchForm(request.GET)
#     if _forms.is_valid():
#         results = _forms.search()
#         log.info(results)
#         res = []
#
#         paginator = ExtentPaginator(results, _count)
#         try:
#             users = paginator.page(_offset)
#         except PageNotAnInteger:
#             users = paginator.page(1)
#         except EmptyPage:
#             return ErrorJsonResponse(status=404)
#         for user in users:
#             # log.info(entity)
#             res.append(
#                 user.v3_toDict()
#             )
#         return SuccessJsonResponse(res)
#
#     return ErrorJsonResponse(status=400)

# @csrf_exempt
# @check_sign
# def unfollow_action(request):
#
#
#     return SuccessJsonResponse()


__author__ = 'edison7500'
