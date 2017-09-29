# coding=utf-8
from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils.log import getLogger
from django.views.decorators.csrf import csrf_exempt
from haystack.generic_views import SearchView

from apps.core.models import Show_Banner, Buy_Link, Selection_Entity, Entity, Entity_Like, Sub_Category
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.views import BaseJsonView, JSONResponseMixin
from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.offline_shop.models import Offline_Shop_Info
from apps.site_banner.models import SiteBanner
from apps.tag.models import Tags
from apps.top_ad.models import TopAdBanner
from apps.v4.forms.pushtoken import PushForm
from apps.v4.forms.search import APISearchForm
from apps.v4.models import APIUser, APISelection_Entity, APIEntity, APICategory, APISeletion_Articles, APIArticle_Dig
from apps.v4.schema.articles import ArticleSchema
from apps.v4.schema.guoku_ad import GKADSchema
from apps.v4.schema.offline_shop import OfflineShop

log = getLogger('django')

article_schema = ArticleSchema(many=False)
ad_schema = GKADSchema(many=True)
offline_shop_schema = OfflineShop(many=True)


def is_taobaoke_url(url):
    return "s.click.taobao.com" in url


def get_taobao_url(taobao_id, is_mobile=False, app_key=None):
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
    @csrf_exempt
    @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(APIJsonView, self).dispatch(request, *args, **kwargs)


class APIJsonSessionView(APIJsonView):
    def check_session(self, request):
        _key = request.REQUEST.get('session', None)
        Session_Key.objects.get(session_key=_key)
        try:
            self.session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist:
            raise

    def get(self, request, *args, **kwargs):
        self.check_session(request)
        return super(APIJsonSessionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_session(request)
        return super(APIJsonSessionView, self).post(request, *args, **kwargs)

    @csrf_exempt
    @check_sign
    def dispatch(self, request, *args, **kwargs):
        try:
            self.check_session(request)
        except Session_Key.DoesNotExist as e:
            return ErrorJsonResponse(data={'message': e.message}, status=403)
        return super(APIJsonSessionView, self).dispatch(request, *args, **kwargs)


class GADView(APIJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        ad = TopAdBanner.objects.ios_top_banners()
        return ad_schema.dump(ad).data

    def get(self, request, *args, **kwargs):
        return super(GADView, self).get(request, *args, **kwargs)


class HomeView(APIJsonView):
    """
    HomeView Class
    This is /mobile/v4/home/ url func
    """
    http_method_names = ['get']

    def get_data(self, context):
        shows = Show_Banner.objects.all()
        articles = APISeletion_Articles.objects.published()
        categories = APICategory.objects.all()
        result = {
            'banner': [{'url': show.banner.url, 'img': show.banner.image_url} for show in shows],
            'articles': [article.api_article.v4_toDict() for article in articles],
            'categories': [category.v4_toDict() for category in categories],
            'entities': [],
        }

        entities = APISelection_Entity.objects.published_until()
        ids = entities.values_list('entity_id', flat=True)
        el = None
        # TODO: 重构！ 重新处理获取喜爱状态的方法
        if self.session is not None:
            el = Entity_Like.objects.user_like_list(user=self.session.user, entity_list=list(ids))

        for row in entities[:5]:
            result['entities'].append({
                'entity': row.entity.v3_toDict(user_like_list=el),
                'note': row.entity.top_note.v3_toDict()
            })
        return result

    def get(self, request, *args, **kwargs):
        _key = self.request.GET.get('session')
        try:
            self.session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist, e:
            self.session = None

        return super(HomeView, self).get(request, *args, **kwargs)


class DiscoverView(APIJsonView):
    """
    DiscoverView Class
    this is '/mobile/v4/discover/' url func
    """

    http_method_names = ['get']

    def get_data(self, context):

        da = APIArticle_Dig.objects.filter(user=self.visitor).values_list('article_id', flat=True)

        result = {
            'banner': [],
            'articles': [],
            'entities': [],
            'categories': [],
            'stores': [],
            'authorizeduser': [],
        }
        # TODO: 恢复对跳转到文章的banner数据增加article数据
        banners = SiteBanner.objects.get_app_banner()
        result['banner'] = [{'url': banner.url, 'img': banner.image_url} for banner in banners]

        popular_articles = APISeletion_Articles.objects.discover()[:3]
        for row in popular_articles:
            article_schema.context['articles_list'] = da
            result['articles'].append({'article': article_schema.dump(row.api_article).data})

        popular_list = Entity_Like.objects.popular_random()
        entities = APIEntity.objects.filter(id__in=popular_list, status=Entity.selection)
        el = Entity_Like.objects.user_like_list(user=self.visitor, entity_list=entities)
        result['entities'] = [{'entity': entity.v4_toDict(user_like_list=el)} for entity in entities]

        categories = APICategory.objects.filter(status=True)
        result['categories'] = [{'category': category.v4_toDict()} for category in categories]

        stores = Offline_Shop_Info.objects.active_offline_shops()
        if stores.count() > 1:
            result['stores'] = offline_shop_schema.dump(stores).data

        auth_users = APIUser.objects.recommended_user()
        result['authorizeduser'] = [{'user': user.v4_toDict(visitor=self.visitor)} for user in auth_users]

        return result

    def get(self, request, *args, **kwargs):
        _key = request.GET.get('session', None)
        self.visitor = None
        if _key is not None:
            try:
                _session = Session_Key.objects.get(session_key=_key)
                self.visitor = _session.user
            except Session_Key.DoesNotExist:
                pass
        return super(DiscoverView, self).get(request, *args, **kwargs)


class AuthorizedUser(APIJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        _key = self.request.GET.get('session')
        self.visitor = None
        try:
            _session = Session_Key.objects.get(session_key=_key)
            self.visitor = _session.user
        except Session_Key.DoesNotExist, e:
            self.visitor = None

        user_list = APIUser.objects.recommended_user()
        paginator = Paginator(user_list, self.size)
        try:
            auth_users = paginator.page(self.page).object_list
        except Exception:
            auth_users = []

        result = {
            'authorized_user': [user.v4_toDict(self.visitor) for user in auth_users],
            'page': self.page,
            'count': user_list.count()
        }
        return result

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.size = request.GET.get('size', 15)
        return super(AuthorizedUser, self).get(request, *args, **kwargs)


@check_sign
def homepage(request):
    shows = Show_Banner.objects.all()
    sub_category = Sub_Category.objects.popular_random(12)
    res = {
        'banner': [{'url': row.banner.url, 'img': row.banner.image_url} for row in shows],
        'discover': [c.v3_toDict() for c in sub_category],
        'hottag': [],
        'config': {
            'taobao_ban_count': 2,
            'url_ban_list': ['http://m.taobao.com/go/act/mobile/cloud-jump.html']
        }}

    return SuccessJsonResponse(data=res)


@check_sign
def selection(request):
    _timestamp = request.GET.get('timestamp', datetime.now())
    if _timestamp is not None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    _key = request.GET.get('session')

    _rcat = request.GET.get('rcat', None)

    if _rcat == '1':
        innqs = Sub_Category.objects.map(group_id_list=[13, 15, 17])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '2':
        innqs = Sub_Category.objects.map(group_id_list=[14, 16])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '3':
        innqs = Sub_Category.objects.map(group_id_list=[26, 28, 29, 30, 31, 32, 34, 35, 36])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '4':
        innqs = Sub_Category.objects.map(group_id_list=[9, 18, 24])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '5':
        innqs = Sub_Category.objects.map(group_id_list=[8, 33])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '6':
        innqs = Sub_Category.objects.map(group_id_list=[21, 22])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '7':
        innqs = Sub_Category.objects.map(group_id_list=[1, 2, 3, 4, 5, 6, 7, 41])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '8':
        innqs = Sub_Category.objects.map(group_id_list=[19, 20])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '9':
        innqs = Sub_Category.objects.map(group_id_list=[10, 11])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '10':
        innqs = Sub_Category.objects.map(group_id_list=[12, 40])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    elif _rcat == '11':
        innqs = Sub_Category.objects.map(group_id_list=[25, 38, 39])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[
                     :30]
    else:
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp)[:30]
    ids = selections.values_list('entity_id', flat=True)

    try:
        _session = Session_Key.objects.get(session_key=_key)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(ids))
        Selection_Entity.objects.set_user_refresh_datetime(session=_session.session_key)
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None
    res = list()

    for selection in selections:
        # TODO： 解决entity可能没有top_note的问题
        if not selection.entity.top_note:
            continue
        r = {
            'entity': selection.entity.v3_toDict(user_like_list=el),
            'note': selection.entity.top_note.v3_toDict(),
        }

        res.append({
            'content': r,
            'post_time': selection.publish_timestamp,
            'type': "note_selection",
        })

    return SuccessJsonResponse(res)


# TODO: Search API
class APISearchView(SearchView, JSONResponseMixin):
    http_method_names = ['get']
    form_class = APISearchForm

    def get_data(self, context):
        res = context.copy()
        return res

    def get(self, request, *args, **kwargs):
        return super(APISearchView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.queryset = form.search()
        return self.render_to_json_response(self.queryset)

    def form_invalid(self, form):
        return ErrorJsonResponse(status=400, data=form.errors)

    @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(APISearchView, self).dispatch(request, *args, **kwargs)


class APISearchHotWordView(APIJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        tags = Tags.objects.hot_article_tags()
        tag_list = [row.name for row in tags]
        return tag_list

    def get(self, request, *args, **kwargs):
        return super(APISearchHotWordView, self).get(request, *args, **kwargs)


# TODO: Popular View API
class PopularView(APIJsonView):
    """
        Get Popular Entity API
    """
    http_method_names = ['get']

    def get_data(self, context):
        popular_list = Entity_Like.objects.popular_random(self.scale)
        entities = APIEntity.objects.filter(id__in=popular_list, status=Entity.selection)

        try:
            _session = Session_Key.objects.get(session_key=self.key)
            el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=entities)
        except Session_Key.DoesNotExist, e:
            log.info(e.message)
            el = None

        res = {
            'content': [{entity.v4_toDict(user_like_list=el) for entity in entities}],
            'scale': self.scale
        }
        return res

    def get(self, request, *args, **kwargs):
        self.scale = request.GET.get('scale', 'daily')
        self.key = request.GET.get('session')
        return super(PopularView, self).get(request, *args, **kwargs)


class TopPopularView(APIJsonView):
    """
        IOS TODAY API
    """
    http_method_names = ['get']

    def __init__(self):
        self._count = 0
        super(TopPopularView, self).__init__()

    @property
    def count(self):
        if not isinstance(self._count, int):
            self._count = int(self._count)
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    def get_data(self, context):
        days = timedelta(days=1)
        now_string = datetime.now().strftime("%Y-%m-%d")
        dt = datetime.now() - days

        query = "select id, entity_id, count(*) as lcount from core_entity_like " \
                "where created_time between '%s' and '%s' group by entity_id order by lcount desc" \
                % (dt.strftime("%Y-%m-%d"), now_string)
        _entity_list = Entity_Like.objects.raw(query).using('slave')

        res = []
        for entity_like in _entity_list[:self.count]:
            r = {
                'entity': entity_like.entity.v3_toDict(),
                'note': entity_like.entity.top_note.v3_toDict()
            }
            res.append({
                'content': r,
                'type': "top_popular",
            })
        return res

    def get(self, request, *args, **kwargs):
        self.count = request.GET.get('count', 30)
        return super(TopPopularView, self).get(request, *args, **kwargs)


class UnreadView(APIJsonSessionView):
    http_method_names = ['get', 'post']

    def get_data(self, context):
        res = {
            'unread_message_count': self.session.user.notifications.read().count(),
            'unread_selection_count': Selection_Entity.objects.get_user_unread(session=self.session.session_key),
        }
        return res


def visit_item(request, item_id):
    _ttid = request.GET.get("ttid", None)
    _sid = request.GET.get("sid", None)
    _outer_code = request.GET.get("outer_code", None)
    _sche = request.GET.get("sche", None)

    b = Buy_Link.objects.filter(origin_id=item_id).first()

    if "taobao.com" in b.origin_source:
        return HttpResponseRedirect(
            decorate_taobao_url(get_taobao_url(b.origin_id, True), _ttid, _sid, _outer_code, _sche))
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
        form = PushForm(user=_user, data=request.POST)
        if form.is_valid():
            form.save()
            return SuccessJsonResponse(data={'message': 'success'})
        for k, v in dict(form.errors).items():
            log.info(v.as_text().split('*'))
            error_msg = v.as_text().split('*')[1]
            return ErrorJsonResponse(status=400, data={'type': k, 'message': error_msg.lstrip()})

        return ErrorJsonResponse(status=403, data={'message': 'error'})
