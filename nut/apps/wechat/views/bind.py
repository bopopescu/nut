from django.views.generic import FormView
from django.views.generic import TemplateView
from apps.wechat.forms.bind import WeChatBindForm


class WeChatBindView(FormView):
    template_name = "wechat/bind.html"
    form_class = WeChatBindForm
    success_url = '/wechat/bind/success/'

    def __init__(self, **kwargs):
        self.open_id = None
        super(WeChatBindView, self).__init__(**kwargs)

    def form_valid(self, form):
        form.bind(self.open_id)
        return super(WeChatBindView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.open_id = kwargs.pop('open_id')
        return super(WeChatBindView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.open_id = kwargs.pop('open_id')
        return super(WeChatBindView, self).post(request, *args, **kwargs)


class WeChatBindSuccessView(TemplateView):
    template_name = "wechat/bind_success.html"
