from django.views.generic import ListView, CreateView, UpdateView, \
                                 DeleteView, View, FormView
from django.views.generic.detail import SingleObjectMixin

from braces.views import StaffuserRequiredMixin, AjaxResponseMixin,\
                         JSONRequestResponseMixin


from apps.notifications.models import DailyPush
from apps.notifications.forms import BaseDailyPushForm
from django.core.urlresolvers import reverse_lazy
from apps.core.models import GKUser
from django.utils.log import getLogger
log = getLogger('django')


class DailyPushCreateView(StaffuserRequiredMixin, CreateView):
    form_class = BaseDailyPushForm
    model = DailyPush
    template_name = 'management/notifications/daily_push_create.html'
    success_url = reverse_lazy('management_push_list')


class DailyPushUpdateView(StaffuserRequiredMixin, UpdateView):
    model = DailyPush
    form_class = BaseDailyPushForm
    template_name = 'management/notifications/daily_push_edit.html'
    success_url = reverse_lazy('management_push_list')

class DailyPushDeleteView(StaffuserRequiredMixin, DeleteView):
    model = DailyPush
    template_name = 'management/notifications/daily_push_delete.html'
    success_url = reverse_lazy('management_push_list')

class DailyPushSendTestView(StaffuserRequiredMixin,\
                            SingleObjectMixin,AjaxResponseMixin, \
                            JSONRequestResponseMixin,View):
    model = DailyPush
    def post_ajax(self, request, *args, **kwargs):
        push_message  = self.get_object()
        test_personals = self.get_request_json().pop('recipients', None)
        try:
            if test_personals :
                users = GKUser.objects.filter(pk__in=test_personals)
                for user in users:
                    push_message.send_jpush_to_user(user)
            return self.render_json_response({
                'error':0
            }, 200)

        except Exception as e:
            log.error('send test message fail %s : user: %s' %(push_message, test_personals))
            return self.render_json_response({
                'error':1,
                'message':'send test message fail'
            }, 500)

        return self.render_json_response({
            'error': 1
        }, 500)




class DailyPushSendProductionView(StaffuserRequiredMixin,
                                  SingleObjectMixin,AjaxResponseMixin, \
                                  JSONRequestResponseMixin, View):

    model = DailyPush
    def post_ajax(self, request, *args, **kwargs):
        push_message  = self.get_object()
        try:
            push_message.send_to_all()
            return self.render_json_response({
                'error':0
            }, 200)
        except Exception as e :
            log.error('send push message error : %s' %e)
            return self.render_json_response({
                'error':1,
                'error_message': "exception: %s" %e
            }, 500)


class DailyPushListView(StaffuserRequiredMixin, ListView):
    context_object_name = 'push_list'
    template_name = 'management/notifications/daily_push_list.html'
    def get_queryset(self):
        return DailyPush.object.all().order_by('-id')


