from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.views.generic import CreateView
from django.utils.log import getLogger

from apps.wechat.models import Robots
from apps.wechat.forms.robots import RobotsForm

log = getLogger('django')

class RobotListView(ListView):

    model = Robots
    template_name = 'management/wechat/list.html'

    def get_context_data(self, **kwargs):
        context = super(RobotListView, self).get_context_data(**kwargs)
        log.info(context)
        return context
    # render_to_response()


class MsgCreateView(CreateView):

    # model = Robots
    form_class = RobotsForm
    template_name = 'management/wechat/create.html'

    def get_form_kwargs(self):
        res = super(MsgCreateView, self).get_form_kwargs()
        log.info(res)
        return res
    # def get_form(self, form_class):
    #     log.info(self.get_form_kwargs())
    #     return form_class()
        # log.info(form_class)
        # return super(MsgCreateView, self).get_form(form_class)

__author__ = 'edison7500'
