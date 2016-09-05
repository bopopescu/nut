from django.core.paginator import Paginator
from django.utils.log import getLogger

from apps.order.models import Order as OrderModel
from apps.v4.views import APIJsonSessionView
from apps.v4.schema.order import OrderSchema

# from pprint import pprint

order_schema = OrderSchema()
log = getLogger('django')


class OrderListView(APIJsonSessionView):

    http_method_names = ['get']

    def get_data(self, context):
        if self.status is None:
            orders = OrderModel.objects.filter(customer=self.session.user)
        else:
            orders = OrderModel.objects.filter(customer=self.session.user, status=self.status)

        paginator = Paginator(orders, self.size)
        try:
            order_list = paginator.page(self.page)
        except Exception as e:
            log.info("<Error: %s>" % e.message)
            return []

        return order_schema.dump(order_list.object_list, many=True).data

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.size = request.GET.get('size', 10)
        self.status = request.GET.get('status', None)

        return super(OrderListView, self).get(request, *args, **kwargs)