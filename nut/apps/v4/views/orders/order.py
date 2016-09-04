from apps.order.models import Order as OrderModel
from apps.v4.views import APIJsonSessionView
from apps.v4.schema.order import OrderSchema

from pprint import pprint

order_schema = OrderSchema()


class CheckOutView(APIJsonSessionView):

    http_method_names = ['post']

    def get_data(self, context):
        _user = self.session.user
        order = _user.checkout()
        # print order_schema.dump(order).data
        pprint(order_schema.dump(order).data, indent=2)
        return order_schema.dump(order, many=False).data

    def get(self, request, *args, **kwargs):
        return super(CheckOutView, self).get(request, *args, **kwargs)


class OrderListView(APIJsonSessionView):

    http_method_names = ['get']

    def get_data(self, context):
        order_list = OrderModel.objects.filter(customer=self.session.user)
        # print order_list
        # print order_schema.dump(order_list).data
        # pprint(order_schema.dump(order_list.first(), many=False).data, indent=2)
        return order_schema.dump(order_list, many=True).data

    def get(self, request, *args, **kwargs):

        return super(OrderListView, self).get(request, *args, **kwargs)