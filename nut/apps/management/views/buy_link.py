from django.http import Http404
from apps.core.views import BaseListView
from apps.core.models import Buy_Link
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage


class BuyLinkListView(BaseListView):

    template_name = 'management/buy_link/list.html'

    # queryset = Buy_Link.objects.filter(status=Buy_Link.sale).order_by('-id')

    def get_queryset(self, **kwargs):
        status = kwargs.pop('status')
        status = int(status)
        self.queryset = Buy_Link.objects.filter(status=status)
        return self.queryset

    def get_status(self, request):
        _status = request.GET.get('status')
        try:
            _status = int(_status)
        except (TypeError, ValueError):
            _status = 2
        return _status

    def get(self, request):
        page = request.GET.get('page', 1)
        status = self.get_status(request)
        _buy_link_list = self.get_queryset(status=status)

        paginator = ExtentPaginator(_buy_link_list, 30)

        try:
            _buy_links = paginator.page(page)
        except InvalidPage:
            _buy_links = paginator.page(1)
        except EmptyPage:
            raise Http404

        context = {
            'buy_links': _buy_links,
            'status': status,
        }
        return self.render_to_response(context)

__author__ = 'edison'
