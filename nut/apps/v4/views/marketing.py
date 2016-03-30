from apps.mobile.models import LaunchBoard
from apps.v4.views import APIJsonView
from apps.mobile.models import Session_Key


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

    def get(self, request, *args, **kwargs):
        _key = request.GET.get('session', None)
        if _key is not None:
            try:
                _session = Session_Key.objects.get(session_key=_key)
                self.visitor = _session.user
            except Session_Key.DoesNotExist:
                self.visitor = None
        return super(LaunchBoardView, self).get(request, *args, **kwargs)


__author__ = 'edison'
