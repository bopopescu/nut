from apps.mobile.models import LaunchBoard
from apps.core.views import BaseJsonView


class LaunchBoardView(BaseJsonView):

    def get_data(self, context):

        return context

__author__ = 'edison'
