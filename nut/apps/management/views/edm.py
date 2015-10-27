#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
import json
from django.template import RequestContext, loader, Context
from django.views.csrf import csrf_failure
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from model_utils.tests.models import Post

from apps.core.models import EDM, Entity_Like, Entity, GKUser
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView, \
    DeleteView
from apps.management.decorators import staff_only
from apps.management.forms.edm import EDMDetailForm
from sendcloud.template import SendCloudTemplate


class EDMListView(ListView):
    model = EDM
    template_name = 'management/edm/list.html'


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


class EDMDelete(DeleteView):
    model = EDM
    success_url = reverse_lazy('management_edm_list')


@login_required
@staff_only
def preview_edm(request, edm_id, template='management/edm/preview.html'):
    if request.method == 'GET':
        edm = get_object_or_404(EDM, pk=edm_id)
        popular_list = Entity_Like.objects.popular_random('monthly', 9)
        entities = Entity.objects.filter(id__in=popular_list)
        return render_to_response(
            template,
            {'edm': edm,
             'popular_entities': entities},
            context_instance=RequestContext(request),
        )


@login_required
@staff_only
def send_edm(request, edm_id):
    pass
    # check_edm_user_list()

@csrf_exempt
@login_required
@staff_only
def approval_edm(request, edm_id):
    edm = get_object_or_404(EDM, pk=edm_id)
    if edm.status not in (edm.waiting_for_sd_verify, edm.sd_verify_failed):
        return "This edm can't approval."

    invoke_name = edm.sd_template_invoke_name
    if not invoke_name:
        invoke_name = 'edm-'+str(edm.publish_time.date())
        invoke_name = invoke_name.replace('-', '_')
        invoke_name = invoke_name.strip()
        edm.sd_template_invoke_name = invoke_name
        edm.save()

    sd_tm = SendCloudTemplate(invoke_name=invoke_name)
    t = loader.get_template('management/edm/preview.html')
    edm = get_object_or_404(EDM, pk=edm_id)
    popular_list = Entity_Like.objects.popular_random('monthly', 9)
    entities = Entity.objects.filter(id__in=popular_list)
    c = Context({'edm': edm, 'popular_list': entities})
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
        # return True
        return HttpResponse('')
    except BaseException, e:
        # return False
        return HttpResponse('')


@csrf_exempt
@login_required
@staff_only
def sync_verify_status(request, edm_id):
    edm = get_object_or_404(EDM, pk=edm_id)
    if edm.status != edm.sd_verifying or not edm.sd_template_invoke_name:
        return "This edm can't sync status."

    sd_tm = SendCloudTemplate(invoke_name=edm.sd_template_invoke_name)
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
    return HttpResponse('')
