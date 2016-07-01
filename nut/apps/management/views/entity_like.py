#- * - coding: utf - 8 -*-
from django.shortcuts import render_to_response
from apps.core.models import Entity_Like
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from apps.core.extend.paginator import ExtentPaginator
from django.utils.log import getLogger
from django.views.generic import ListView
from datetime import datetime, timedelta

class EntityLikeView():
    template_name = 'management/selection_report/entity_like.html'
    model = Entity_Like
    # paginate_by = 40
    context_object_name = 'Entity_Like'
    # paginator_class = ExtentPaginator

    def _(requst):
        post = Entity_Like.objects.all()
        #self.id = self.request.GET.get('id')
        content = {'post':post}
        #entity_id = self.request.GET.get("entity_id")
        #use_id = self.request.GET.get("user_id")

        return render_to_response('entity_like.html', content)