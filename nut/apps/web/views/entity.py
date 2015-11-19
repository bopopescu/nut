# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect, \
    HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apps.core.utils.http import JSONResponse

from apps.core.models import Entity, Entity_Like, Note, Note_Comment, \
    Note_Poke, Brand, Buy_Link
from apps.core.tasks.entity import like_task, unlike_task
from apps.web.forms.comment import CommentForm
from apps.web.forms.note import NoteForm
from apps.web.forms.entity import EntityURLFrom, CreateEntityForm, ReportForms

from apps.web.utils.viewtools import add_side_bar_context_data
from apps.tag.models import Content_Tags

from django.views.generic.detail import DetailView

from django.views.generic import RedirectView
from braces.views import AjaxResponseMixin, JSONResponseMixin

from django.conf import settings
from django.utils.log import getLogger


log = getLogger('django')


class EntityCard(AjaxResponseMixin, JSONResponseMixin, DetailView):
    template_name = 'web/entity/entity_card.html'

    def get_object(self, queryset=None):
        _entity_hash = self.kwargs.get('entity_hash', None)
        if _entity_hash is None:
            raise Exception('can not find hash')
        _entity = Entity.objects.get(entity_hash=_entity_hash,
                                     status__gte=Entity.freeze)
        return _entity

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


def entity_detail(request, entity_hash, templates='web/entity/detail.html'):
    _entity_hash = entity_hash

    _user = None
    _note_forms = None
    _user_pokes = list()

    try:
        _entity = Entity.objects.prefetch_related('notes').get(entity_hash=_entity_hash,
                                     status__gte=Entity.freeze)\


    except Entity.DoesNotExist:
        raise Http404

    nid_list = _entity.notes.all().values_list('id', flat=True)
    if request.user.is_authenticated():
        _user = request.user
        # pop up a note form if there is a note in entity's notes submit by current user .
        # add by an , for user posted note pop up
        _notes = Note.objects.filter(user=_user, entity=_entity)

        if len(_notes) > 0:
            _note_forms = NoteForm(instance=_notes[0])
        else:
            _note_forms = NoteForm()
        _user_pokes = Note_Poke.objects.filter(note_id__in=list(nid_list),
                                               user=request.user).values_list(
            'note_id', flat=True)
        # log.info(_user_pokes)

    # tags = Content_Tags.objects.filter(target_object_id__in=list(nid_list))[:10]

    tags = Content_Tags.objects.entity_tags(list(nid_list))[:10]

    _user_post_note = True
    try:
        _entity.notes.get(user=_user)
    except Note.DoesNotExist:
        _user_post_note = False

    like_status = 0
    try:
        _entity.likes.get(user=_user)
        like_status = 1
    except Entity_Like.DoesNotExist:
        pass

    _guess_entities = Entity.objects.guess(category_id=_entity.category_id,
                                           count=9, exclude_id=_entity.pk)

    context = {
        'entity': _entity,
        'like_status': like_status,
        # 'user':_user,
        'user_pokes': _user_pokes,
        'user_post_note': _user_post_note,
        'note_forms': _note_forms or NoteForm(),
        'guess_entities': _guess_entities,
        # 'likers': _entity.likes.all()[:13],
        'is_entity_detail': True,
        'tags': tags,
        # 'entity_brand': get_entity_brand(_entity),
        # 'pop_tags' : _pop_tags
    }
    context = add_side_bar_context_data(context)
    return render_to_response(
        templates,
        context,
        context_instance=RequestContext(request),
    )


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
            return JSONResponse(data={'result': '1'})
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
                el = Entity_Like.objects.create(
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
        try:
            if settings.DEBUG:
                el = Entity_Like.objects.get(entity_id=eid, user=_user)
                el.delete()
            else:
                unlike_task.delay(uid=_user.id, eid=eid)
            return JSONResponse(data={'status': 0})
        except Entity_Like.DoesNotExist:
            raise Http404

        return HttpResponseNotAllowed


@login_required
def entity_create(request, template="web/entity/new.html"):
    if request.method == 'POST':
        # user = request.user
        # if user.is_active < 1:
        #     return HttpResponse("你妹")


        _forms = CreateEntityForm(request=request, data=request.POST)
        if _forms.is_valid():
            entity = _forms.save()

            return HttpResponseRedirect(
                reverse('web_entity_detail', args=[entity.entity_hash, ]))
        log.info(_forms.errors)
        raise 500
    else:
        _url_froms = EntityURLFrom(request)

        return render_to_response(
            template,
            {
                'url_forms': _url_froms
            },
            context_instance=RequestContext(request),
        )


@login_required
def entity_load(request):
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

    raise HttpResponseNotAllowed


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
        return b.link

    def get(self, request, *args, **kwargs):
        if not request.META.has_key('HTTP_REFERER'):
            return HttpResponseForbidden()
        if 'guoku.com' not in request.META['HTTP_REFERER']:
            raise Http404
        self.buy_id = kwargs.pop('buy_id', None)
        assert self.buy_id is not None
        return super(gotoBuyView, self).get(request, *args, **kwargs)


__author__ = 'edison'
