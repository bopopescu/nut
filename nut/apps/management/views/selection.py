# -*- coding: utf-8 -*-
import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apps.core.models import Selection_Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, \
    EmptyPage
from apps.core.forms.selection import SelectionForm, SetPublishDatetimeForm
from apps.management.decorators import admin_only
from apps.core.utils.http import ErrorJsonResponse, SuccessJsonResponse

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View

from datetime import datetime, timedelta
# import json

from django.utils.log import getLogger


log = getLogger('django')


@login_required
def published(request, template="management/selection/list.html"):
    _page = request.GET.get('page', 1)

    s = Selection_Entity.objects.published()
    # log.info(s.query)
    paginator = ExtentPaginator(s, 30)

    try:
        selections = paginator.page(_page)
    except PageNotAnInteger:
        selections = paginator.page(1)
    except EmptyPage:
        raise Http404

    # log.info(selections.object_list)
    # innqs = selections.object_list
    # _entities = Entity.objects.filter(id__in=list(selections.object_list))

    return render_to_response(
        template,
        {
            'selections': selections,
            'pending_count': Selection_Entity.objects.pending().count(),
            'pending_and_removed_count': Selection_Entity.objects.pending_and_removed().count()
            # 'entities': _entities,
        },
        context_instance=RequestContext(request)
    )


@login_required
def pending(request, template="management/selection/list.html"):
    _page = request.GET.get('page', 1)
    s = Selection_Entity.objects.pending()
    # log.info(s.query)
    paginator = ExtentPaginator(s, 30)

    try:
        selections = paginator.page(_page)
    except PageNotAnInteger:
        selections = paginator.page(1)
    except EmptyPage:
        raise Http404

    # _entities = Entity.objects.filter(id__in=list(selections.object_list))

    return render_to_response(
        template,
        {
            'selections': selections,
            'pending_count': Selection_Entity.objects.pending().count(),
            'pending_and_removed_count': Selection_Entity.objects.pending_and_removed().count()
            # 'entities': _entities,
        },
        context_instance=RequestContext(request)
    )


@login_required()
def pending_and_removed(request, template="management/selection/list.html"):
    _page = request.GET.get('page', 1)
    s = Selection_Entity.objects.pending_and_removed()
    paginator = ExtentPaginator(s, 30)

    try:
        selections = paginator.page(_page)
    except PageNotAnInteger:
        selections = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'selections': selections,
            'pending_count': Selection_Entity.objects.pending().count(),
            'pending_and_removed_count': s.count()
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_publish(request, sid,
                 template="management/selection/edit_publish.html"):
    # return HttpResponse("OK")
    try:
        selection = Selection_Entity.objects.get(pk=sid)
    except Selection_Entity.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = SelectionForm(selection=selection, data=request.POST)
        if _forms.is_valid():
            _forms.update()

    else:
        _forms = SelectionForm(selection=selection)
        # print dir(_forms['pub_time'])
        # print _forms['pub_time'].name
    return render_to_response(
        template,
        {
            'selection': selection,
            'forms': _forms,
            'button': _('update'),
        },
        context_instance=RequestContext(request)
    )


class PrepareBatchSelection(JSONResponseMixin, AjaxResponseMixin, View):
    template_name = 'management/selection/batch_selection.html'

    def get_entity_list(self, id_list):
        '''
        :type id_list: list , a python list contain "Entity" id list ,
                              then use this id list filter Selection_Entity's Pending List
                              again , the result will be a pure Python list of dictionary , Not Query set
        :return:
        '''
        selection_entities = Selection_Entity.objects.pending().filter(
            entity__pk__in=id_list)
        entities = [sle.entity.pickToDict('id', 'title', 'chief_image',
                                          'category_name', 'top_note_string')
                    for sle in selection_entities]
        return entities

    def get_last_selection(self):
        selection_entity = Selection_Entity.objects.published().first()
        res = selection_entity.entity.pickToDict('id', 'title', 'chief_image',
                                                 'category_name')
        res.update(
            {'pub_time': selection_entity.pub_time.strftime('%Y-%m-%d %H:%M')})
        return res

    def post_ajax(self, request, *args, **kwargs):
        entity_ids_jsonstring = request.POST.get('entity_id_list', None)
        if not entity_ids_jsonstring:
            res = {
                'error': 1,
                'msg': _('can not get entity id list'),
            }
            return self.render_json_response(res)

        list_entity_ids = json.loads(entity_ids_jsonstring)
        entities = self.get_entity_list(list_entity_ids)
        res = {
            'data': {
                'entities': entities,
                'last_published_entity': self.get_last_selection(),
            },
            'error': 0,
        }
        return self.render_json_response(res)


class RemoveBatchSelection(AjaxResponseMixin, JSONResponseMixin, View):

    def doRemoveSelectionBatch(self, entity_id_list):
        published_selections = Selection_Entity.objects.published().filter(
            entity__id__in=entity_id_list)
        for sla in published_selections:
            sla.is_published = False
            sla.save()
        return

    def post_ajax(self, request, *args, **kwargs):
        remove_id_list_jsonstring = request.POST.get('entity_id_list', None)
        if not remove_id_list_jsonstring:
            res = {
                'error': 1,
                'msg': 'can not get remove id list json string'
            }
            return self.render_json_response(res)
        remove_list = json.loads(remove_id_list_jsonstring)
        if remove_list:
            try:
                self.doRemoveSelectionBatch(remove_list)
            except Exception as e:
                res = {
                    'error': 1,
                    'msg': 'error %s' % e.message
                }
                return self.render_json_response(res)
            res = {
                'error': 0,
                'msg': 'remove selection Success'
            }
            return self.render_json_response(res)
        else:
            res = {
                'error': 1,
                'msg': 'can not get remove list from json string'
            }
            return self.render_json_response(res)


class DoBatchSelection(AjaxResponseMixin, JSONResponseMixin, View):
    def doBatchMission(self, batch_mission):
        for mission in batch_mission:
            sla = Selection_Entity.objects.pending().filter(
                entity__pk=mission['id']).get()
            sla.is_published = True
            sla.pub_time = mission['pub_time']
            sla.save()
        return

    def post_ajax(self, request, *args, **kwargs):
        batch_mission_jsonstring = request.POST.get('batch_list', None)
        if not batch_mission_jsonstring:
            res = {
                'error': 1,
                'msg': 'can not get batch data',
            }
            return self.render_json_response(res)
        batch_mission = json.loads(batch_mission_jsonstring)
        if batch_mission:
            try:
                self.doBatchMission(batch_mission)
            except Exception as e:
                res = {
                    'error': 1,
                    'msg': 'error: %s' % e.message
                }
                return self.render_json_response(res)
            res = {
                'error': 0,
                'msg': u'精选商品发布成功',
            }
            return self.render_json_response(res)
        else:
            res = {
                'error': 1,
                'msg': 'can not get batch list from data, contact admin',
            }
            return self.render_json_response(res)


@csrf_exempt
@login_required
@admin_only
def batch_selection(request,
                    template='management/selection/batch_selection.html'):
    if request.is_ajax():
        pass
    log.info('test for batch_selection');


@login_required
def set_publish_datetime(request,
                         template="management/selection/set_publish_datetime.html"):
    if request.is_ajax():
        template = "management/selection/set_publish_datetime.html"

    if request.method == "POST":
        _forms = SetPublishDatetimeForm(request.POST)
        if _forms.is_valid():
            _forms.save()
            return HttpResponseRedirect(
                reverse('management_selection_published'))
    else:
        _forms = SetPublishDatetimeForm()

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance=RequestContext(request)
    )


@login_required
def popular(request, template="management/selection/popular.html"):
    days = timedelta(days=7)
    now_string = datetime.now().strftime("%Y-%m-%d")
    dt = datetime.now() - days

    query = "select id, entity_id, count(*) as lcount from core_entity_like where created_time between '%s' and '%s' group by entity_id order by lcount desc" % (
        dt.strftime("%Y-%m-%d"), now_string)
    _entity_list = Entity_Like.objects.raw(query)

    log.info(_entity_list.query)
    # for like in  entity_list:
    # log.info(like.entity )

    return render_to_response(
        template,
        {
            'popular_entity_list': _entity_list[:60],
            'pending_count': Selection_Entity.objects.pending().count(),
            'pending_and_removed_count': Selection_Entity.objects.pending_and_removed().count()
        },
        context_instance=RequestContext(request)
    )


@csrf_exempt
@login_required
@admin_only
def usite_published(request):
    if request.is_ajax():
        entityids_json = request.POST.get('eids', None)
        # log.info(entityids_json)
        from apps.core.tasks import usite_published
        # usite_published(entityids_json)
        usite_published.delay(entityids_json)
        # print json.loads(entityids_json)
        return SuccessJsonResponse(data={'status': 'ok'})
    else:
        return ErrorJsonResponse(status=400)


__author__ = 'edison7500'
