from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse

from apps.wechat.models import Robots
from apps.wechat.forms.reply import ReplyForm


class ReplyListView(ListView):

    template_name = "management/wechat/replylist.html"
    model = Robots

    # def get(self, request, *args, **kwargs):
    #
    #     return super(ReplyListView, self).get(request, *args, **kwargs)


class CreateReplyView(CreateView):

    template_name = "management/wechat/reply_create.html"
    model = Robots
    form_class = ReplyForm

    def get_success_url(self):
        return reverse('management_wechat_reply')


class EditReplyView(UpdateView):

    template_name = "management/wechat/reply_edit.html"
    # form_class =
    form_class = ReplyForm
    model = Robots

    def get_success_url(self):
        return reverse('management_wechat_reply')