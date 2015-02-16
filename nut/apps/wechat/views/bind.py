from django.views.generic import FormView
from django.utils.log import getLogger

from apps.wechat.forms.bind import WeChatBindForm


log = getLogger('django')


class WeChatBindView(FormView):

    template_name = "wechat/bind.html"
    form_class = WeChatBindForm

    # def form_valid(self, form):

        # return super(WeChatBindView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        # self.open_id = request.session.get('open_id')
        self.open_id = kwargs.pop('open_id')
        return super(WeChatBindView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.open_id = kwargs.pop('open_id')
        return super(WeChatBindView, self).post(request, *args, **kwargs)

    def get_initial(self):
        # log.info("open id %s" % self.open_id)
        initial =  super(WeChatBindView, self).get_initial()
        initial['open_id'] = self.open_id
        return initial


__author__ = 'edison'
