from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.views.generic import CreateView
from django.utils.log import getLogger
from apps.wechat.models import Robots


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

    model = Robots


__author__ = 'edison7500'
