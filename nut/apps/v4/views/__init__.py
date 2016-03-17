#coding=utf-8
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Show_Banner, \
    Buy_Link, Selection_Entity, Entity, \
    Entity_Like, Sub_Category

from apps.v4.models import APIUser, APISelection_Entity, APIEntity, APICategory, APISeletion_Articles, APIAuthorized_User_Profile
from apps.v4.forms.pushtoken import PushForm
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from apps.core.views import BaseJsonView



from django.utils.log import getLogger
log = getLogger('django')


def is_taobaoke_url(url):
    return "s.click.taobao.com" in url

def get_taobao_url(taobao_id, is_mobile = False, app_key = None):
    url = ""
    if is_mobile:
        url = "http://a.m.taobao.com/i%s.htm" % taobao_id
    else:
        url = "http://item.taobao.com/item.htm?id=%s" % taobao_id
        if app_key:
            url += "&spm=2014.%s.0.0" % app_key
    return url

def decorate_taobao_url(url, ttid=None, sid=None, outer_code=None, sche=None):
    if sche:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&sche=%s" % sche
    if ttid:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&ttid=%s" % ttid
    if sid:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&sid=%s" % sid
    if is_taobaoke_url(url) and outer_code:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&unid=%s" % outer_code

    return url


class APIJsonView(BaseJsonView):

    @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(APIJsonView, self).dispatch(request, *args, **kwargs)


class HomeView(APIJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        res = dict()
        shows = Show_Banner.objects.all()
        res['banner'] = []
        for row in shows:
            res['banner'].append(
                {
                    'url':row.banner.url,
                    'img':row.banner.image_url
                }
            )
        res['articles'] = []
        articles = APISeletion_Articles.objects.published()
        for row in articles[:3]:
            res['articles'].append(
                row.api_article.v4_toDict()
            )

        res['categories'] = []
        categories = APICategory.objects.all()
        for row in categories[:3]:
            res['categories'].append(
                row.v4_toDict()
            )

        res['entities'] = []
        entities = APISelection_Entity.objects.published_until()
        ids = entities.values_list('entity_id', flat=True)

        el = None
        if self.session is not  None:
            el = Entity_Like.objects.user_like_list(user=self.session.user, entity_list=list(ids))

        for row in entities[:5]:
            r = {
                'entity': row.entity.v3_toDict(user_like_list=el),
                'note': row.entity.top_note.v3_toDict(),
            }
            res['entities'].append(
                r
            )
        return res

    def get(self, request, *args, **kwargs):
        _key = self.request.GET.get('session')
        try:
            self.session = Session_Key.objects.get(session_key=_key)
            # Selection_Entity.objects.set_user_refresh_datetime(session=self.session.session_key)
        except Session_Key.DoesNotExist, e:
            self.session = None

        return super(HomeView, self).get(request, *args, **kwargs)


class DiscoverView(APIJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        _key = self.request.GET.get('session')

        res = dict()
        shows = Show_Banner.objects.all()
        res['banner'] = []
        for row in shows:
            res['banner'].append(
                {
                    'url':row.banner.url,
                    'img':row.banner.image_url
                }
            )

        '''
        get Popular Articles List
        '''
        res['articles'] = list()
        popular_articles = APISeletion_Articles.objects.discover()[:3]
        for row in popular_articles:
            print type(row)
            r = {
                'article': row.api_article.v4_toDict()
            }
            res['articles'].append(r)

        '''
        get Popular Entity List
        '''
        popular_list = Entity_Like.objects.popular_random()
        _entities = APIEntity.objects.filter(id__in=popular_list, status=Entity.selection)
        try:
            _session = Session_Key.objects.get(session_key=_key)
            el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=_entities)
        except Session_Key.DoesNotExist, e:
            # log.info(e.message)
            el = None

        res['entities'] = list()
        for e in _entities:
            r = {
                'entity': e.v4_toDict(user_like_list=el)
            }
            res['entities'].append(r)

        '''
        get Category
        '''
        res['categories'] = list()
        # categories = APICategory.objects.filter(status=True)
        categories = APICategory.objects.popular()
        log.info(categories)
        for row in categories:
            r = {
                'category': row.v4_toDict(),
            }
            res['categories'].append(r)


        '''
        get authorizeduser
        '''
        res['authorizeduser'] = list()

        auth_users = APIUser.objects.recommended_user()

        # user APIUser -> GKUser ->  GKUserManager interface query

        # a user in Authorized_User_Profile table does not mean he is a authorized user .
        # a user in Author or Seller group mean he is a authorized user

        # auth_users = APIAuthorized_User_Profile\
        #                 .objects.recommended_authorized_users()[:8]

        for user in auth_users:
            r = {
                'user': user.v4_toDict()
            }
            # print r
            res['authorizeduser'].append(r)
            # print row.user.v4_toDict()
        return res


class AuthorizedUser(APIJsonView):

    http_method_names = ['get']

    def get_data(self, context):
        _key = self.request.GET.get('session')
        self.visitor = None
        try:
            _session = Session_Key.objects.get(session_key=_key)
            self.visitor = _session.user
        except Session_Key.DoesNotExist, e:
            log.info(e.message)
            self.visitor = None

        res = dict()
        res['authorized_user'] = list()
        res['page'] = self.page
        # res['size'] = self.size
        user_list = APIUser.objects.recommended_user()
        res['count'] = user_list.count()

        paginator = Paginator(user_list, self.size)
        try:
            auth_users = paginator.page(self.page)
        except Exception:
            return res

        for user in auth_users.object_list:
            res['authorized_user'].append(
                user.v4_toDict(self.visitor)
            )
        return res

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.size = request.GET.get('size', 15)
        return super(AuthorizedUser, self).get(request, *args, **kwargs)


@check_sign
def homepage(request):

    res = dict()
    shows = Show_Banner.objects.all()
    res['banner'] = []
    for row in shows:
        res['banner'].append(
            {
                'url':row.banner.url,
                'img':row.banner.image_url
            }
        )

    res['discover'] = []
    sub_category = Sub_Category.objects.popular_random(12)
    log.info(sub_category)
    for c in sub_category:
        res['discover'].append(
            c.v3_toDict()
        )
    # log.info(res['discover'])
    res['hottag'] = []

    res['config'] = {}
    res['config']['taobao_ban_count'] = 2
    res['config']['url_ban_list'] = ['http://m.taobao.com/go/act/mobile/cloud-jump.html']
    return SuccessJsonResponse(data=res)


@check_sign
def selection(request):
    # log.info(request.GET)
    # _timestamp = request.GET.get('timestamp', None)
    _timestamp = request.GET.get('timestamp', datetime.now())
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    _key = request.GET.get('session')

    _count = int(request.GET.get('count'))
    _rcat = request.GET.get('rcat', None)
    log.info("rcat %s" % _rcat)

    if _rcat == '1':
        innqs = Sub_Category.objects.map(group_id_list=[13, 15, 17])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '2':
        # innqs = Sub_Category.objects.filter(group_id__in=[14, 16]).values_list('id', flat=True)
        innqs = Sub_Category.objects.map(group_id_list=[14, 16])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '3':
        innqs = Sub_Category.objects.map(group_id_list=[26, 28, 29, 30, 31, 32, 34, 35, 36])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '4':
        innqs = Sub_Category.objects.map(group_id_list=[9, 18, 24])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '5':
        innqs = Sub_Category.objects.map(group_id_list=[8, 33])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '6':
        innqs = Sub_Category.objects.map(group_id_list=[21, 22])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '7':
        innqs = Sub_Category.objects.map(group_id_list=[1, 2, 3, 4, 5, 6, 7, 41])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '8':
        innqs = Sub_Category.objects.map(group_id_list=[19, 20])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '9':
        innqs = Sub_Category.objects.map(group_id_list=[10, 11])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '10':
        innqs = Sub_Category.objects.map(group_id_list=[12, 40])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '11':
        innqs = Sub_Category.objects.map(group_id_list=[25, 38, 39])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    else:
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp)[:30]
    ids = selections.values_list('entity_id', flat=True)

    try:
        _session = Session_Key.objects.get(session_key=_key)
        # log.info("session %s" % _session)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(ids))
        log.info(_session.session_key)
        Selection_Entity.objects.set_user_refresh_datetime(session=_session.session_key)
    except Session_Key.DoesNotExist, e:
        # log.info(e.message)
        el = None
    # log.info(el)
    res = list()

    for selection in selections:
        # if (selection.entity.tio)
        r = {
            'entity':selection.entity.v3_toDict(user_like_list=el),
            'note':selection.entity.top_note.v3_toDict(),
        }

        res.append({
            'content': r,
            'post_time': selection.publish_timestamp,
            'type': "note_selection",
        })

    return SuccessJsonResponse(res)


@check_sign
def popular(request):

    _scale = request.GET.get('scale', 'daily')
    _key = request.GET.get('session')
    log.info(_scale)
    popular_list = Entity_Like.objects.popular_random(_scale)
    _entities = APIEntity.objects.filter(id__in=popular_list, status=Entity.selection)

    try:
        _session = Session_Key.objects.get(session_key=_key)
        # log.info("session %s" % _session)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=_entities)
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None


    res = dict()
    res['content'] = list()
    res['scale'] = _scale
    for e in _entities:
        r = {
            'entity': e.v4_toDict(user_like_list=el)
        }
        res['content'].append(r)

    return SuccessJsonResponse(res)


@check_sign
def toppopular(request):

    days = timedelta(days=1)
    now_string = datetime.now().strftime("%Y-%m-%d")
    dt = datetime.now() - days
    _count = request.GET.get('count')
    _count = int(_count)

    query = "select id, entity_id, count(*) as lcount from core_entity_like where created_time between '%s' and '%s' group by entity_id order by lcount desc" % (dt.strftime("%Y-%m-%d"), now_string)
    _entity_list = Entity_Like.objects.raw(query).using('slave')

    res = []
    for entity_like in _entity_list[:_count]:
        r = {
            'entity': entity_like.entity.v3_toDict(),
            'note': entity_like.entity.top_note.v3_toDict()
        }
        res.append({
            'content': r,
            'type': "top_popular",
        })

    return SuccessJsonResponse(res)

# @check_sign
# def unread(request):
#
#     _key = request.GET.get('session')
#
#     try:
#         _session = Session_Key.objects.get(session_key = _key)
#     except Session_Key.DoesNotExist:
#         return ErrorJsonResponse(status=403)
#
#     res = {
#         'unread_message_count': _session.user.notifications.read().count(),
#         'unread_selection_count': Selection_Entity.objects.get_user_unread(session=_session.session_key),
#     }
#     return SuccessJsonResponse(res)

class UnreadView(APIJsonView):

    def get_data(self, context):
        try:
            _session = Session_Key.objects.get(session_key = self.key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)
        res = {
            'unread_message_count': _session.user.notifications.read().count(),
            'unread_selection_count': Selection_Entity.objects.get_user_unread(session=_session.session_key),
        }
        return res

    def get(self, request, *args, **kwargs):
        self.key = request.GET.get('session', None)
        if self.key is None:
          return ErrorJsonResponse(status=403)
        return super(UnreadView, self).get(request, *args, **kwargs)


def visit_item(request, item_id):
    _ttid = request.GET.get("ttid", None)
    _sid = request.GET.get("sid", None)
    _entry = request.GET.get("entry", "mobile")
    _outer_code = request.GET.get("outer_code", None)
    _sche = request.GET.get("sche", None)

    b = Buy_Link.objects.filter(origin_id=item_id).first()

    if "taobao.com" in b.origin_source:
        # _taobaoke_info = taobaoke_mobile_item_convert(b.origin_id)
        # if _taobaoke_info and _taobaoke_info.has_key('click_url'):
        #     return HttpResponseRedirect(decorate_taobao_url(_taobaoke_info['click_url'], _ttid, _sid, _outer_code, _sche))
        return HttpResponseRedirect(decorate_taobao_url(get_taobao_url(b.origin_id, True), _ttid, _sid, _outer_code, _sche))
    if "jd.com" in b.origin_source:
        _jd_url = "http://item.m.jd.com/product/%s.html" % b.origin_id
        return HttpResponseRedirect(_jd_url)

    if "amazon" in b.origin_source:
        return HttpResponseRedirect(b.amazon_url)

    if "6pm" in b.origin_source:
        url = b.link.replace('www', 'm')
        return HttpResponseRedirect(url)

    else:
        return HttpResponseRedirect(b.link)


@csrf_exempt
@check_sign
def apns_token(request):

    if request.method == 'POST':
        _key = request.POST.get('session', None)
        _user = None
        try:
            _session = Session_Key.objects.get(session_key=_key)
            _user = _session.user
        except Session_Key.DoesNotExist:
            pass
            # return ErrorJsonResponse(status=403)
        log.info(request.POST)
        form = PushForm(user=_user, data=request.POST)
        if form.is_valid():
            form.save()
            return SuccessJsonResponse(data={'message':'success'})
        # log.info(form.errors)
        for k, v in dict(form.errors).items():
            log.info(v.as_text().split('*'))
            error_msg = v.as_text().split('*')[1]
            return ErrorJsonResponse(status=400, data={
                'type': k,
                'message': error_msg.lstrip(),
            })

        return ErrorJsonResponse(status=403, data={'message':'error'})


__author__ = 'edison7500'
