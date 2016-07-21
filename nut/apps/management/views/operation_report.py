# -*- coding: utf-8 -*-


from apps.core.models import  GKUser, Entity, Note, Article, Article_Remark, Entity_Like
from django.utils.log import getLogger
from django.views.generic import View
from django.db.models import  Count
from datetime import datetime, timedelta
from braces.views import UserPassesTestMixin
from django.views.generic.base import TemplateResponseMixin

log = getLogger('django')

TIME_FORMAT = '%Y-%m-%d 00:00:00'


class OperationReportListView(UserPassesTestMixin, TemplateResponseMixin, View):
    template_name = 'management/operation_report/list.html'

    def test_func(self, user):
        return user.is_admin

    def get_context_data(self, *args, **kwargs):
        context = {}
        self.status = self.request.GET.get('status', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get("end_date")
        if start_date == 'lastmonth':
            self.start_time = start_date
            self.start_date, self.end_date = ((datetime.now() - timedelta(days=30)).strftime(TIME_FORMAT)), (
            datetime.now() + timedelta(days=1)).strftime(TIME_FORMAT)
        elif start_date and end_date:
            self.start_time = None
            self.start_date, self.end_date = start_date, end_date
        else:
            self.start_time = 'lastweek'
            self.start_date, self.end_date = ((datetime.now() - timedelta(days=7)).strftime(TIME_FORMAT)), (
                datetime.now() + timedelta(days=1)).strftime(TIME_FORMAT)
        context['auth_seller_count'] = GKUser.objects.authorized_seller().using('slave').count()
        context['auth_author_count'] = GKUser.objects.authorized_author().using('slave').count()
        context['active_user_count'] = GKUser.objects.active_user().using('slave').count()
        context['new_auth_seller_count'] = GKUser.objects.authorized_seller().using('slave').filter(
            date_joined__range=(self.start_date, self.end_date)).count()
        context['new_auth_author_count'] = GKUser.objects.authorized_author().using('slave').filter(
            date_joined__range=(self.start_date, self.end_date)).count()
        context['new_active_user_count'] = GKUser.objects.active_user().using('slave').filter(
            date_joined__range=(self.start_date, self.end_date)).count()
        context['entity_count'] = Entity.objects.using('slave').filter(
            created_time__range=(self.start_date, self.end_date), status__gt=-1).count()
        context['note_count'] = Note.objects.using('slave').filter(
            post_time__range=(self.start_date, self.end_date)).count()
        entitys = Entity.objects.using('slave').filter(likes__created_time__range=(self.start_date, self.end_date))
        context['entity_count_100'] = entitys.annotate(likes_count=Count('likes')).filter(likes_count__gte=100).count()
        context['entity_count_50'] = entitys.annotate(likes_count=Count('likes')).filter(likes_count__gte=50).count()
        articles = Article.objects.using('slave').filter(updated_datetime__range=(self.start_date, self.end_date), publish=2)
        context['article_count'] = articles.count()
        context['article_read'] = articles.filter(read_count__gt=1000).count()
        context['article_dig'] = Article.objects.using('slave').filter(digs__created_time__range=(self.start_date, self.end_date)).\
            annotate(digs_count=Count('digs')).filter(digs_count__gte=10).count()
        context['article_remark_count'] = Article_Remark.objects.using('slave').filter(
            create_time__range=(self.start_date, self.end_date)).count()
        context['status'] =  self.status
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['start_time'] = self.start_time
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)