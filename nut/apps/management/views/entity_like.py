#- * - coding: utf - 8 -*-

from apps.core.models import Selection_Entity, Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator
from django.utils.log import getLogger
from django.views.generic import ListView
from datetime import datetime, timedelta

from haystack.query import SearchQuerySet

class EntityLikeView():
    template_name = 'management/selection_report/list.html'
    model = Entity_Like
    # paginate_by = 40
    context_object_name = 'Entity_Like'
    # paginator_class = ExtentPaginator

    def get_query(self):
        self.id = self.request.GET.get('id', None)
        entity_id = self.request.GET.get('entity_id', None)
        use_id = self.request.GET.get("user_id")
        return use_id
