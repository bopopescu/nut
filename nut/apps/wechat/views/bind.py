from django.views.generic import FormView
from apps.wechat.forms.bind import WeChatBindForm


class WeChatBindView(FormView):

    template_name = "wechat/bind.html"
    form_class = WeChatBindForm

    # def form_valid(self, form):

        # return super(WeChatBindView, self).form_valid(form)

    def get(self, request, *args, **kwargs):

        return super(WeChatBindView, self).get(request, *args, **kwargs)





__author__ = 'edison'
