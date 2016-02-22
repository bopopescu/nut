from apps.mobile.models import LaunchBoard
from apps.v4.views import APIJsonView


class LaunchBoardView(APIJsonView):

    def get_data(self, context):
        res = {}
        agent_string = self.request.META.get('HTTP_USER_AGENT', None)
        if 'guoku-client' in agent_string:
            launch = LaunchBoard.objects.filter(device=LaunchBoard.android, status=True).first()
        elif 'orange' in agent_string:
            launch = LaunchBoard.objects.filter(device=LaunchBoard.ios, status = True).first()
        else:
            launch = LaunchBoard.objects.filter(device=LaunchBoard.all, status=True).first()

        if launch:
            res['launch_id'] = launch.pk
            res['title'] = launch.title
            res['description'] = launch.description
            res['version'] = launch.version
            res['action_title'] = launch.action_title
            res['action'] = launch.action
            res['launch_image_url'] = launch.launch_image_url
            return res
        return None


__author__ = 'edison'
