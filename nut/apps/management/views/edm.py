#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.utils.log import getLogger
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView

from apps.core.models import EDM, Entity_Like, Entity, SD_Address_List
from apps.management.decorators import staff_only
from apps.management.forms.edm import EDMDetailForm
from sendcloud import template as sd_template


log = getLogger('django')


class EDMListView(ListView):
    model = EDM
    template_name = 'management/edm/list.html'
    queryset = EDM.objects.filter(display=True)


class EDMCreate(CreateView):
    model = EDM
    form_class = EDMDetailForm
    template_name = 'management/edm/detail.html'
    success_url = reverse_lazy('management_edm_list')


class EDMUpdate(UpdateView):
    model = EDM
    form_class = EDMDetailForm
    template_name = 'management/edm/detail.html'
    success_url = reverse_lazy('management_edm_list')


@csrf_exempt
@login_required
@staff_only
def edm_delete(request, edm_id):
    response_data = {'result': 'succeed', 'message': ''}
    edm = get_object_or_404(EDM, pk=edm_id)
    if edm.status not in (edm.waiting_for_sd_verify, edm.sd_verify_succeed,
                          edm.sd_verify_failed):
        response_data['result'] = 'failed'
        response_data['message'] = "This edm can't be deleted."
    else:
        edm.display = False
        edm.save()
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@login_required
@staff_only
def preview_edm(request, edm_id, template='management/edm/preview.html'):
    if request.method == 'GET':
        edm = get_object_or_404(EDM, pk=edm_id)
        popular_list = Entity_Like.objects.popular_random('monthly', 9)
        entities = Entity.objects.filter(id__in=popular_list)
        site_host = request.get_host()
        return render_to_response(
            template,
            {'edm': edm,
             'host': site_host,
             'popular_entities': entities},
            context_instance=RequestContext(request),
        )


@csrf_exempt
@login_required
@staff_only
def send_edm(request, edm_id):
    response_data = {'result': 'succeed', 'message': ''}
    edm = get_object_or_404(EDM, pk=edm_id)
    if edm.status != edm.sd_verify_succeed:
        response_data['result'] = 'failed'
        response_data['message'] = "This edm can't be sent. " \
                                   "please contact administrators."
    else:
        all_addr_list = SD_Address_List.objects.all()
        for address in all_addr_list:
            to = address.address
            invoke_name = edm.sd_template_invoke_name
            sd_tm = sd_template.SendCloudTemplate(invoke_name=invoke_name,
                                      edm_user=settings.MAIL_EDM_USER)
            result = sd_tm.send_to_list(edm.title,
                                        settings.GUOKU_MAIL,
                                        settings.GUOKU_NAME,
                                        to)
            if not result or result['message'] != 'success':
                response_data['result'] = 'failed'
                if 'message' in response_data:
                    response_data['message'] += ';'.join(result['errors'])
                else:
                    response_data['message'] = ';'.join(result['errors'])
                log.error(u"Send email to address list %s failed."
                          u" More information: %s", to, result)
            else:
                edm.status = edm.send_completed
                edm.sd_task_id = result['mail_list_task_id_list']
                edm.save()
                sd_tm.delete()
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")
#
#
# @csrf_exempt
# @login_required
# @staff_only
# def check_send_status(request, edm_id):
#     response_data = {'result': 'succeed', 'message': ''}
#     edm = get_object_or_404(EDM, pk=edm_id)
#     if edm.status != edm.sending:
#         response_data['result'] = 'failed'
#         response_data['message'] = "This edm didn't sended anything."
#     else:
#         invoke_name = edm.sd_template_invoke_name
#         sd_tm = SendCloudTemplate(invoke_name=invoke_name)
#         sd_tm.check_task(edm.sd_task_id)
#     return HttpResponse(json.dumps(response_data),
#                         content_type="application/json")


@csrf_exempt
@login_required
@staff_only
def approval_edm(request, edm_id):
    response_data = {'result': 'succeed', 'message': ''}
    edm = get_object_or_404(EDM, pk=edm_id)
    if edm.status not in (edm.waiting_for_sd_verify, edm.sd_verify_failed):
        response_data['result'] = 'failed'
        response_data['message'] = "This edm can't approval."
    else:
        invoke_name = edm.sd_template_invoke_name
        if not invoke_name:
            invoke_name = 'edm-%d-%s' % (edm.id, str(edm.publish_time.date()))
            invoke_name = invoke_name.replace('-', '_')
            invoke_name = invoke_name.strip()
            edm.sd_template_invoke_name = invoke_name
            edm.save()

        sd_tm = sd_template.SendCloudTemplate(invoke_name=invoke_name,
                                  edm_user=settings.MAIL_EDM_USER)
        t = loader.get_template('management/edm/preview.html')
        popular_list = Entity_Like.objects.popular_random('monthly', 9)
        entities = Entity.objects.filter(id__in=popular_list)
        site_host = request.get_host()
        c = Context(
            {'edm': edm, 'popular_entities': entities, 'host': site_host})
        html = t.render(c)

        data = {
            'name': u'edm - %s版' % str(edm.publish_time.date()).strip(),
            'html': html,
            'subject': edm.title,
        }
        try:
            sd_tm.update_or_create(**data)
            edm.status = edm.sd_verifying
            edm.save()
        except BaseException, e:
            response_data['result'] = 'failed'
            response_data['message'] = e.message
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@csrf_exempt
@login_required
@staff_only
def sync_verify_status(request, edm_id):
    response_data = {'result': 'succeed', 'message': ''}
    edm = get_object_or_404(EDM, pk=edm_id)
    if edm.status != edm.sd_verifying or not edm.sd_template_invoke_name:
        response_data['result'] = 'failed'
        response_data['message'] = "This edm can't sync status."
    else:
        sd_tm = sd_template.SendCloudTemplate(
            invoke_name=edm.sd_template_invoke_name,
            edm_user=settings.MAIL_EDM_USER)
        status = sd_tm.get_status()
        if status == 1:
            edm.status = edm.sd_verify_succeed
        elif status == 0:
            edm.status = edm.sd_verifying
        elif status == -1:
            edm.status = edm.sd_verify_failed
        elif status == -2:
            edm.status = edm.waiting_for_sd_verify
        edm.save()
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")
