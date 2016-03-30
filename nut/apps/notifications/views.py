from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template import loader
from django.db.models import Count

from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import Entity_Like, Entity, Sub_Category, GKUser
from apps.core.utils.http import JSONResponse
from apps.core.extend.paginator import ExtentPaginator as Jpaginator
from apps.web.utils.viewtools import add_side_bar_context_data

from datetime import datetime
import random


from django.utils.log import getLogger

log = getLogger('django')

from braces.views import AjaxResponseMixin, JSONResponseMixin,LoginRequiredMixin
from django.views.generic import ListView

class MessageListView(LoginRequiredMixin, AjaxResponseMixin,JSONResponseMixin, ListView):
    template_name = 'notifications/messages/message.html'
    ajax_template_name = 'notifications/messages/partial/ajax_notification.html'
    paginator_class =  Jpaginator
    paginate_by = 15
    context_object_name = 'messages'

    def get_ajax(self, request, *args, **kwargs):
        self.object_list = getattr(self,'object_list', self.get_queryset())
        context = self.get_context_data()
        _template = self.ajax_template_name
        _t = loader.get_template(_template)
        _c = RequestContext(request, context)
        _html = _t.render(_c)
        res = {'status': 1,
                'data': _html
               }
        return self.render_json_response(res)

    def get_queryset(self):
        _timestamp = self.get_timestamp()

        remove_user_list = [self.request.user.pk]
        message_list =  self.request.user.notifications.filter(timestamp__lt=_timestamp)\
                       .exclude(actor_object_id__in=remove_user_list)

        # mark all message as read
        self.request.user.notifications.mark_all_as_read()

        return message_list

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context = add_side_bar_context_data(context)
        return context

    def get_timestamp(self):
        _ts = self.request.GET.get('timestamp', None)
        if _ts is None:
            return datetime.now()
        else:
            return datetime.fromtimestamp(float(_ts))




@require_GET
@login_required
def messages(request, template='notifications/messages/message.html'):
    _user = request.user
    _page = request.GET.get('page', 1)
    _timestamp = request.GET.get('timestamp',None)
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    else:
        _timestamp = datetime.now()

    el = Entity_Like.objects.popular()
    cids = Entity.objects.filter(pk__in=list(el)).annotate(dcount=Count('category')).values_list('category_id', flat=True)

    _categories = Sub_Category.objects.filter(id__in=list(cids), status=True)
    # too expensive ???

    # remove_user_list = GKUser.objects.deactive_user_list()
    # remove_user_list.append(_user.id)
    # remove_user_list = list(remove_user_list)
    remove_user_list = []
    remove_user_list.append(_user.id)
    message_list = _user.notifications.filter(timestamp__lt=_timestamp).exclude(actor_object_id__in=remove_user_list)

    paginator = ExtentPaginator(message_list, 15)

    try:
        _messages = paginator.page(_page)
    except PageNotAnInteger:
        _messages = paginator.page(1)
    except EmptyPage:
        raise Http404

    _user.notifications.mark_all_as_read()
    if request.is_ajax():
        if not _messages.object_list:
            res = {
                'status': 0,
                'msg': 'no data'
            }
        else:
            _t = loader.get_template('notifications/messages/partial/ajax_notification.html')
            _c = RequestContext(request, {
                'messages': _messages,
            })
            _data = _t.render(_c)
            res = {
                'status': 1,
                'data': _data,
            }
        return JSONResponse(data=res, content_type='text/html; charset=utf-8',)

    return render_to_response(
        template,
        {
            'messages': _messages,
            'categories': random.sample(_categories, 6),
            # 'category': category,
        },
        context_instance = RequestContext(request),
    )


__author__ = 'edison'
