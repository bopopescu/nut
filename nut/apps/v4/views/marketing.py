from apps.mobile.models import LaunchBoard
from apps.core.views import BaseJsonView
from apps.mobile.lib.sign import check_sign


class LaunchBoardView(BaseJsonView):

    def get_data(self, context):
        res = {}
        launch = LaunchBoard.objects.filter(status = True).first()
        if launch:
            res['title'] = launch.title
            res['description'] = launch.description
            res['action'] = launch.action
        return res

    # @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(LaunchBoardView, self).dispatch(request, *args, **kwargs)

__author__ = 'edison'
