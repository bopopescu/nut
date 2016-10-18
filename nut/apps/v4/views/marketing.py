from apps.mobile.models import LaunchBoard
from apps.v4.views import APIJsonView
from apps.mobile.models import Session_Key
# from apps.top_ad.models import TopAdBanner

from apps.v4.schema.launch import LaunchSchema


launch_schema   = LaunchSchema(many=False)


from apps.v4.schema.guoku_ad import GKADSchema
ad_scheme       = GKADSchema(many=True)


class LaunchBoardView(APIJsonView):

    def get_data(self, context):
        agent_string = self.request.META.get('HTTP_USER_AGENT', None)
        if 'guoku-client' in agent_string:
            launch = LaunchBoard.objects.filter(device=LaunchBoard.android, status=True).first()
        elif 'orange' in agent_string:
            launch = LaunchBoard.objects.filter(device=LaunchBoard.ios, status = True).first()
        else:
            launch = LaunchBoard.objects.filter(device=LaunchBoard.all, status=True).first()

        if launch:
            return launch_schema.dump(launch).data


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
