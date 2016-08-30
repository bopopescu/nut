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

    # def get(self, request, *args, **kwargs):
    #     return super(CartListView, self).get(request, args, **kwargs)



class AddSKUToCartView(APIJsonSessionView):

    http_method_names = ['post']

    def get_data(self, context):
        form = CartForm(self.request.POST)
        if form.is_valid():
            form.save(user=self.session.user)
            return {'status': True}
        return ErrorJsonResponse(data=form.errors ,status=401)
