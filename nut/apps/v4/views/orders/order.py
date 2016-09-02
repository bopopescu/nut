from apps.order.models import Order as OrderModel
from apps.v4.views import APIJsonSessionView
from apps.v4.schema.order import OrderSchema

order_schema = OrderSchema()


class CheckOutView(APIJsonSessionView):

    http_method_names = ['post']

    def get_data(self, context):

        return

    def get(self, request, *args, **kwargs):
        return super(CheckOutView, self).get(request, *args, **kwargs)


class OrderListView(APIJsonSessionView):

    http_method_names = ['get']

    def get_data(self, context):
        order_list = OrderModel.objects.filter(customer=self.session.user)

        return order_schema.dump(order_list).data

    def get(self, request, *args, **kwargs):

        return super(OrderListView, self).get(request, *args, **kwargs)