from apps.core.views import BaseListView
from apps.core.models import Buy_Link

class BuyLinkListView(BaseListView):

    template_name = 'management/buy_link/list.html'

    queryset = Buy_Link.objects.all()


__author__ = 'edison'
