#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from django.views.csrf import csrf_failure
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from model_utils.tests.models import Post

from apps.core.models import EDM, Entity_Like, Entity, GKUser
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView, \
    DeleteView
from apps.management.decorators import staff_only
from apps.management.forms.edm import EDMDetailForm


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
        edm = EDM.objects.filter(id=edm_id)
        popular_list = Entity_Like.objects.popular_random('monthly', 9)
        entities = Entity.objects.filter(id__in=popular_list)
        if edm:
            edm = edm[0]
        else:
            raise 404
        return render_to_response(
            template,
            {'edm': edm,
             'popular_entities': entities},
            context_instance=RequestContext(request),
        )


@login_required
@staff_only
def send_edm(request, edm_id):
    check_edm_user_list()


@csrf_exempt
@login_required
@staff_only
def check_edm_user_list(request):
    if request.method == 'POST':
        gk_users_count = GKUser.objects.filter(is_active__gte=1).count()
        # sd_user_count =
        print '>> count: ', gk_users_count
        response_data = {}
        response_data['result'] = 'Create post successful!'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
