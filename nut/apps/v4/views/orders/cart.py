from apps.core.views import ErrorJsonResponse
from apps.v4.views import APIJsonSessionView
from apps.v4.models import APICartItem
from apps.v4.forms.entity_sku import CartForm


class CartListView(APIJsonSessionView):

    def get_data(self, context):
        _user = self.session.user

        items = APICartItem.objects.filter(user=_user)

        res = list()

        for row in items:
            res.append(
                row.v4_toDict()
            )
        return res


class AddSKUToCartView(APIJsonSessionView):

    http_method_names = ['post']

    def get_data(self, context):
        form = CartForm(self.request.POST)
        if form.is_valid():
            form.save(user=self.session.user)
            return {'status': True}
        return ErrorJsonResponse(data=form.errors ,status=401)


class ClearCartView(APIJsonSessionView):

    http_method_names = ['post']

    def get_data(self, context):
        _user = self.session.user
        _user.clear_cart()
        return {'status': True}
