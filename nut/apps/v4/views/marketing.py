from apps.mobile.models import LaunchBoard
from apps.core.views import BaseJsonView
from apps.mobile.lib.sign import check_sign
# from apps.core.utils.http import ErrorJsonResponse


class LaunchBoardView(BaseJsonView):

    def get_data(self, context):
        res = {}
        launch = LaunchBoard.objects.filter(status = True).first()
        if launch:
            res['launch_id'] = launch.pk
            res['title'] = launch.title
            res['description'] = launch.description
            res['action_title'] = launch.action_title
            res['action'] = launch.action
            res['launch_image_url'] = launch.launch_image_url
            return res
        return None

    @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(LaunchBoardView, self).dispatch(request, *args, **kwargs)

__author__ = 'edison'
