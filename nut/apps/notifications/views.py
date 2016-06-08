# encoding: utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template import loader
from django.db.models import Count

from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import Entity_Like, Entity, Sub_Category, GKUser, Note, Note_Comment, Note_Poke, Article
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

        # for test
        messages = context.get('messages')

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

        # data = []
        # for m in message_list:
        #     if m.action_object_content_type.model == 'selection_entity':
        #         data.append({'type': 'selection_entity', 'entity_id': m.target.id, 'entity_hash': m.target.entity_hash,
        #                      'entity_image': m.target.chief_image, 'entity_title': m.target.title})
        #     elif m.action_object_content_type.model == 'user_follow':
        #         data.append({'type': 'user_follow', 'user_id': m.actor.id, 'username': m.actor.profile.nick,
        #                      'user_avatar': m.actor.profile.avatar_url})
        #     elif m.action_object_content_type.model in ('note', 'entity_like'):
        #         data.append({'type': m.action_object_content_type.model, 'user_id': m.actor.id,
        #                      'username': m.actor.profile.nick,
        #                      'user_avatar': m.actor.profile.avatar_url, 'entity_id': m.target.id,
        #                      'entity_hash': m.target.entity_hash,
        #                      'entity_image': m.target.chief_image, 'entity_title': m.target.title})
        #     elif m.action_object_content_type.model in ('note_comment', 'note_poke'):
        #         data.append({'type': m.action_object_content_type.model, 'user_id': m.actor.id,
        #                      'username': m.actor.profile.nick,
        #                      'user_avatar': m.actor.profile.avatar_url, 'entity_id': m.target.entity.id,
        #                      'entity_hash': m.target.entity.entity_hash,
        #                      'entity_image': m.target.entity.chief_image, 'entity_title': m.target.entity.title})
        #     elif m.action_object_content_type.model == 'article_dig':
        #         data.append({'type': m.action_object_content_type.model, 'user_id': m.actor.id,
        #                      'username': m.actor.profile.nick,
        #                      'user_avatar': m.actor.profile.avatar_url, 'article_id': m.targer.id,
        #                      'article_cover': m.target.cover_url,
        #                      'article_title': m.target.title})
        # d = []
        # for m in message_list:
        #     if isinstance(m.target, Note):
        #         d.append({'target': { 'type': 'note', 'id': m.target.entity.id, 'entity_hash': m.target.entity.entity_hash, 'entity_image': m.target.entity.chief_image,
        #                              'entity_title': m.target.entity.title},
        #                   'actor': {'id': m.actor.id, 'nick': m.actor.profile.nick, 'avatar': m.actor.avatar_url},
        #                   'type': m.action_object_content_type.model})
        #     elif isinstance(m.target, Entity):
        #         d.append({'target': {'type': 'entity', 'id': m.target.id, 'entity_hash': m.target.entity_hash, 'entity_image': m.target.chief_image,
        #                              'entity_title': m.target.title},
        #                   'actor': {'id': m.actor.id, 'nick': m.actor.profile.nick, 'avatar': m.actor.avatar_url},
        #                   'type': m.action_object_content_type.model})
        #     elif isinstance(m.target, Article):
        #         d.append({'target': {'type': 'article', 'id': m.target.id, 'article_cover': m.target.cover_url,
        #                      'article_title': m.target.title},
        #                   'actor': {'id': m.actor.id, 'nick': m.actor.profile.nick, 'avatar': m.actor.avatar_url},
        #                   'type': m.action_object_content_type.model})
        #     elif isinstance(m.target, GKUser):   # 被关注
        #         d.append({'actor': {'id': m.actor.id, 'nick': m.actor.profile.nick, 'avatar': m.actor.avatar_url},
        #                   'type': m.action_object_content_type.model})


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


class NewMessageListView(LoginRequiredMixin, AjaxResponseMixin,JSONResponseMixin, ListView):
    paginator_class =  Jpaginator
    paginate_by = 20
    context_object_name = 'messages'

    def get_ajax(self, request, *args, **kwargs):
        self.object_list = getattr(self,'object_list', self.get_queryset())
        context = self.get_context_data()
        messages = context.get('messages')
        data = []
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'
        host = protocol + '://' + request.get_host()
        try:
            for m in messages:
                if isinstance(m.target, Note):
                    data.append({'target': {'type': 'note', 'id': m.target.entity.id,
                                         'entity_hash': m.target.entity.entity_hash,
                                         'entity_image': m.target.entity.chief_image,
                                         'entity_title': m.target.entity.title, 'url': host+m.target.entity.get_absolute_url()},
                              'actor': {'id': m.actor.id, 'nick': m.actor.profile.nick, 'avatar': m.actor.avatar_url,
                                        'url': host + m.actor.absolute_url},
                              'type': m.action_object_content_type.model,
                              'time': m.timesince().split(u'，')[0]})
                elif isinstance(m.target, Entity):
                    data.append({'target': {'type': 'entity', 'id': m.target.id, 'entity_hash': m.target.entity_hash,
                                         'entity_image': m.target.chief_image, 'url': host+m.target.get_absolute_url(),
                                         'entity_title': m.target.title},
                              'actor': {'id': m.actor.id, 'nick': m.actor.profile.nick, 'avatar': m.actor.avatar_url,
                                        'url': host+m.actor.absolute_url},
                              'type': m.action_object_content_type.model,
                              'time': m.timesince().split(u'，')[0]})
                elif isinstance(m.target, Article):
                    data.append({'target': {'type': 'article', 'id': m.target.id, 'article_cover': m.target.cover_url,
                                         'article_title': m.target.title, 'url': host+m.target.get_absolute_url()},
                              'actor': {'id': m.actor.id, 'nick': m.actor.profile.nick, 'avatar': m.actor.avatar_url,
                                        'url': host + m.actor.absolute_url},
                              'time': m.timesince().split(u'，')[0],
                              'type': m.action_object_content_type.model})
                elif isinstance(m.target, GKUser):
                    data.append({'actor': {'id': m.actor.id, 'nick': m.actor.profile.nick, 'avatar': m.actor.avatar_url,
                                           'url': host + m.actor.absolute_url},
                              'type': m.action_object_content_type.model,
                              'time': m.timesince().split(u'，')[0]})

            res = {'status': 1,
                    'data': data
                   }
        except:
            res = {'status': 0}
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
        context = super(NewMessageListView, self).get_context_data(**kwargs)
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

    paginator = ExtentPaginator(message_list, 5)

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
