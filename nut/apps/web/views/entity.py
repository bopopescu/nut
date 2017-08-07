# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect, \
    HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from apps.core.utils.http import JSONResponse
from apps.core.views import BaseJsonView

from apps.core.models import Entity, Entity_Like, Note, Note_Comment, \
    Note_Poke, Brand, Buy_Link
from apps.core.tasks.entity import like_task, unlike_task
from apps.web.forms.comment import CommentForm
from apps.web.forms.note import NoteForm
from apps.web.forms.entity import EntityURLFrom, CreateEntityForm, ReportForms

from apps.web.utils.viewtools import add_side_bar_context_data
from apps.tag.models import Content_Tags

from django.views.generic.detail import DetailView
from django.views.generic import RedirectView, ListView, View
from braces.views import AjaxResponseMixin, JSONResponseMixin, LoginRequiredMixin

from django.conf import settings
from django.utils.log import getLogger

import requests


log = getLogger('django')
taobao_recommendation_url = getattr(settings, 'TAOBAO_RECOMMEND_URL', None)


class EntityDetailMixin(object):
    def get_object(self, queryset=None):
        _entity_hash = self.kwargs.get('entity_hash', None)
        if _entity_hash is None:
            raise Exception('can not find hash')
        _entity = get_object_or_404(Entity, entity_hash=_entity_hash,status__gte=Entity.freeze)
        # _entity = Entity.objects.get(entity_hash=_entity_hash,
        #                              status__gte=Entity.freeze)
        return _entity

class EntityLikersView(EntityDetailMixin,ListView):
    template_name = 'web/entity/entity_likers_list.html'
    paginate_by = 12
    context_object_name = 'entity_likes'

    def get_queryset(self):
        entity = self.get_object()
        return entity.likes.all()

    def get_context_data(self, **kwargs):
        context = super(EntityLikersView, self).get_context_data()
        context['entity'] = self.get_object()
        context = add_side_bar_context_data(context)
        return context


class EntitySaleView(EntityDetailMixin, DetailView):
    context_object_name = 'entity'
    template_name = 'web/entity/entity_sale.html'
    def get_context_data(self, **kwargs):
        context = super(EntitySaleView, self).get_context_data(**kwargs)
        context['current_host'] = settings.SITE_HOST
        return context


class EntityCard(AjaxResponseMixin, JSONResponseMixin, EntityDetailMixin, DetailView):
    template_name = 'web/entity/entity_card.html'

    def get(self, request, *args, **kwargs):
        _entity_hash = self.kwargs.get('entity_hash', None)
        return HttpResponseRedirect(
            reverse('web_entity_detail', args=[_entity_hash]))

    def get_ajax(self, request, *args, **kwargs):
        _entity = None
        data = {}
        try:
            _entity = self.get_object()
        except Exception as e:
            data = {
                'error': 1,
                'message': e.message
            }
            return self.render_json_response(data);

        # entity is ok now
        t = loader.get_template(template_name=self.template_name)
        c = RequestContext(request, {
            'entity': _entity
        })
        html = t.render(c)
        data = {
            'error': 0,
            'html': html
        }
        return self.render_json_response(data)


def get_entity_brand(entity):
    if not bool(entity.brand):
        return None
    brand_list = Brand.objects.filter(name__contains=entity.brand)
    if brand_list:
        return brand_list[0]
    return None



class NewEntityDetailView(EntityDetailMixin, DetailView):
    template_name = 'web/entity/detail.html'
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(NewEntityDetailView,self).get_context_data()
        context['like_status'] = self.get_like_status(context)
        context['user_pokes'] = self.get_user_pokes(context)
        context['note_forms'] = self.get_note_forms(context)
        context['user_post_note'] = self.get_is_user_post_note(context)
        context['guess_entities'] = self.get_guess_entities(context)
        context['is_entity_detail'] = True
        context['tags'] = self.get_entity_tags(context)
        context['entity_brand'] = self.get_entity_brand(context)
        context = add_side_bar_context_data(context)
        return context

    def get_is_user_post_note(self,context):
        if not self.request.user.is_authenticated():
            return False
        _entity = context['entity']
        _user_post_note = True
        try:
            _entity.notes.get(user=self.request.user)
        except Note.DoesNotExist as e:
            _user_post_note = False
        except Note.MultipleObjectsReturned as e:
            _user_post_note = True
        return _user_post_note

    def get_like_status(self, context):
        like_status = 0
        if not self.request.user.is_authenticated():
            return like_status

        _entity = context['entity']
        try:
            _entity.likes.get(user=self.request.user)
            like_status = 1
        except Entity_Like.DoesNotExist:
            pass
        return like_status

    def get_note_forms(self, context):
        _entity = context['entity']

        if self.request.user.is_authenticated():
            _user = self.request.user
            _notes = Note.objects.filter(user=_user, entity=_entity)
            if len(_notes) >0:
                _note_forms = NoteForm(instance=_notes[0])
            else:
                 _note_forms = NoteForm()
            return _note_forms
        else :
            return NoteForm()


    def get_user_pokes(self, context):
        _entity = context['entity']
        nid_list = _entity.notes.all().values_list('id', flat=True)
        self._nid_list = nid_list
        if self.request.user.is_authenticated():
            return Note_Poke.objects.filter(note_id__in=list(nid_list),
                                            user=self.request.user)\
                                    .values_list('note_id', flat=True)
        else:
            return list()

    def get_guess_entities(self, context):
        _entity = context['entity']
        return Entity.objects.guess(category_id=_entity.category_id,
                                           count=9, exclude_id=_entity.pk)

    def get_entity_tags(self, context):
        _entity = context['entity']
        return Content_Tags.objects.entity_tags(list(self._nid_list))[:10]

    def get_entity_brand(self, context):
        _entity = context['entity']
        brand = None
        if _entity.brand_id and _entity.brand_id != 'NOT_FOUND':
            brand = Brand.objects.get(id=_entity.brand_id)
        return brand


def wap_entity_detail(request, entity_hash, template='wap/detail.html'):
    return HttpResponseRedirect(
        reverse('web_entity_detail', args=[entity_hash]))


def wechat_entity_detail(request, entity_id, template='wap/detail.html'):
    # _entity_id = int(entity_id)
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404
    return HttpResponseRedirect(
        reverse('web_entity_detail', args=[_entity.entity_hash]))


def tencent_entity_detail(request, entity_hash,
                          template='tencent/detail.html'):
    return HttpResponseRedirect(
        reverse('web_entity_detail', args=[entity_hash]))


@login_required
def entity_post_note(request, eid,
                     template='web/entity/partial/ajax_detail_note.html'):
    if request.method == 'POST':
        _user = request.user
        _eid = eid

        _forms = NoteForm(request.POST, user=_user, eid=_eid)
        if _forms.is_valid():
            note = _forms.save()
            _t = loader.get_template(template)
            _c = RequestContext(request, {
                'note': note,
                'note_forms': _forms
            })
            _data = _t.render(_c)
            return JSONResponse(
                data={
                    'status': 1,
                    'data': _data,
                },
                content_type='application/json; charset=utf-8',
            )
    raise HttpResponseNotAllowed


@login_required
def entity_update_note(request, nid):
    if request.method == "POST":
        _user = request.user
        _forms = NoteForm(request.POST, user=_user, nid=nid)
        if _forms.is_valid():
            note = _forms.update()
            return JSONResponse(data={'result': '1', 'note':note.note})
    # else:
    return HttpResponseNotAllowed


# @login_required
def entity_note_comment(request, nid,
                        template='web/entity/note/comment_list.html'):
    # _user = None
    if request.method == "POST":
        if request.user.is_authenticated():
            _user = request.user
        else:
            return HttpResponseRedirect(reverse('web_login'))

        try:
            note = Note.objects.get(pk=nid)
        except Note.DoesNotExist:
            raise Http404
        _forms = CommentForm(note=note, user=_user, data=request.POST)
        if _forms.is_valid():
            # log.info("ok ok ok ok")

            comment = _forms.save()
            template = 'web/entity/note/comment.html'

            _t = loader.get_template(template)
            _c = RequestContext(request, {
                'comment': comment,
            })

            _data = _t.render(_c)

            return JSONResponse(
                data={
                    'data': _data,
                    'status': '1',
                },
                content_type='text/html; charset=utf-8',
            )
            # log.info(_forms.errors)
            # return
    else:
        _forms = CommentForm()

    _comment_list = Note_Comment.objects.filter(note_id=nid).normal()
    log.info(_comment_list.query)
    # log.info(_comment_list)
    _t = loader.get_template(template)
    _c = RequestContext(request, {
        'comment_list': _comment_list,
        'note_id': nid,
        'forms': _forms
        # 'note_context': _note_context,
    })
    _data = _t.render(_c)

    return JSONResponse(
        data={
            'data': _data,
            'note_id': nid
        },
        content_type='text/html; charset=utf-8',
    )


@login_required
def entity_note_comment_delete(request, comment_id):
    if request.is_ajax():
        _user = request.user
        try:
            comment = Note_Comment.objects.get(user=_user, pk=comment_id)
            comment.delete()
            return JSONResponse(data={'status': 1})
        except:
            raise Http404

    return HttpResponseNotAllowed


@login_required
@csrf_exempt
def entity_like(request, eid):
    if request.is_ajax():
        _user = request.user
        try:
            # try:
            # Entity_Like.objects.get(user_id=_user.id, entity_id=eid)
            # except Entity_Like.DoesNotExist, e:
            # obj = Entity_Like.objects.create(
            # user_id = _user.id,
            #             entity_id = eid,
            #         )
            #         obj.entity.innr_like()
            # return obj
            if settings.DEBUG:
                el, created = Entity_Like.objects.get_or_create(
                    user=_user,
                    entity_id=eid,
                )

            else:
                like_task.delay(uid=_user.id, eid=eid)

            return JSONResponse(data={'status': 1})
        except Exception, e:
            log.error("ERROR: %s", e.message)

    return HttpResponseNotAllowed


@login_required
@csrf_exempt
def entity_unlike(request, eid):
        if request.is_ajax():
            _user = request.user
        else:
            return HttpResponseNotAllowed
        try:
            if settings.DEBUG:
                el = Entity_Like.objects.get(entity_id=eid, user=_user)

                el.delete()
            else:
                unlike_task.delay(uid=_user.id, eid=eid)
            return JSONResponse(data={'status': 0})
        except Entity_Like.DoesNotExist:
            raise Http404

        # return HttpResponseNotAllowed



@login_required
def entity_create(request, template="web/entity/new.html"):
    if request.user.is_authenticated and request.user.is_active < 1:
        return HttpResponseForbidden()
    if request.method == 'POST':

        _forms = CreateEntityForm(request=request, data=request.POST)
        if _forms.is_valid():
            entity = _forms.save()

            return HttpResponseRedirect(
                reverse('web_entity_detail', args=[entity.entity_hash, ]))
        log.info(_forms.errors)
        raise Exception('')
    else:
        _url_froms = EntityURLFrom(request)

        return render_to_response(
            template,
            {
                'url_forms': _url_froms
            },
            context_instance=RequestContext(request),
        )


class EntityCreateView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        _forms = CreateEntityForm(request=request, data=request.POST)
        if _forms.is_valid():
            entity = _forms.save()
            return self.render_json_response({
                'entity_url':entity.absolute_url,
                'errors': 0
            })

        else:
            return self.render_json_response({
                'errors': 1,
                'error_desc': _forms.errors
            }, 403)



class CaptchaRefreshView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin, View):
    # this need to be refactored into a micro service
    def post_ajax(self, request, *args, **kwargs):
        to_json_response = {}
        to_json_response['captcha_0'] = CaptchaStore.generate_key()
        to_json_response['captcha_img_url'] = captcha_image_url(to_json_response['captcha_0'])
        return self.render_json_response(to_json_response)

@login_required
def entity_captcha_refresh(request):
    pass

def get_user_load_key(user):
    return 'timer:user:load_entity_url:%s' % user.id



@login_required
def entity_load(request):
    key = get_user_load_key(request.user)
    # debouncing using cache timeout
    loading = cache.get(key)
    if loading:
        return JSONResponse(data={'error':'too many request'}, status=403)
    else :
        # after captcha , block user in 2 seconds
        cache.set(key ,True , timeout=2)
        pass
    #debouncing end

    if request.method == "POST":
        _forms = EntityURLFrom(request=request, data=request.POST)
        if _forms.is_valid():
            _item_info = _forms.load()
            # log.info(_item_info)
            if 'entity_hash' in _item_info:
                _res = {
                    'status': 'EXIST',
                    'data': _item_info,
                }
            else:
                _res = {
                    'status': 'SUCCESS',
                    'data': _item_info,
                }
            return JSONResponse(data=_res)

    return JSONResponse(data={'error':'request method not right'},status=403)


@login_required
def report(request, eid, template="web/entity/report.html"):
    if not request.is_ajax():
        return HttpResponseNotAllowed(permitted_methods='')
    entity = get_object_or_404(Entity, pk=eid)

    _user = request.user
    log.info(_user)
    if request.method == "POST":
        _form = ReportForms(entity, data=request.POST)
        if _form.is_valid():
            _form.save(_user)
            return HttpResponse("success")
    else:
        _form = ReportForms(entity)

    return render_to_response(
        template,
        {
            'form': _form,
            'entity': entity,
        },
        context_instance=RequestContext(request),
    )


class gotoBuyView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        b = Buy_Link.objects.get(pk=self.buy_id)

        if "amazon" in b.origin_source:
            return b.amazon_url
        elif "kaola" in b.origin_source:
            return b.kaola_url
        return b.link

    def get(self, request, *args, **kwargs):
        if not request.META.has_key('HTTP_REFERER'):
            return HttpResponseForbidden()
        if 'guoku.com' not in request.META['HTTP_REFERER']:
            raise Http404
        self.buy_id = kwargs.pop('buy_id', None)
        assert self.buy_id is not None
        return super(gotoBuyView, self).get(request, *args, **kwargs)


# TODO: taobao recommendation api
class TaobaoRecommendationView(BaseJsonView):

    def get_data(self, context):

        payload = {
            'keyword': self.keyword,
            'mall': self.mall,
            'count': self.count,
        }
        if self.user_id:
            payload.update({'uid': self.user_id})
        r = requests.get(taobao_recommendation_url, params=payload)
        try:
            data = r.json()
        except ValueError:
            data = {}
        return data

    def get(self, request, *args, **kwargs):
        # self.keyword = kwargs.pop('keyword', None)
        self.keyword = request.GET.get('keyword', None)
        assert self.keyword is not None
        self.mall = request.GET.get('mall', False)
        self.count = request.GET.get('count', 12)
        if request.user.is_authenticated():
            self.user_id = request.user.id
        else:
            self.user_id = None
        # self.mall = kwargs.pop('mall', False)
        return super(TaobaoRecommendationView, self).get(requests, *args, **kwargs)

# class DesignWeekAPIView(EntityDetailMixin, RedirectView):
#     def get(self, request, *args, **kwargs):
#         entity_hash = kwargs.get('entity_hash')
#         referer = request.META.get('HTTP_REFERER')
#         user_id = request.user.id
#         entity_id = self.get_object().id
#         click_record.delay(user_id, entity_id, referer)
#         return HttpResponseRedirect(reverse('web_entity_detail', args=[entity_hash]))





__author__ = 'edison'
