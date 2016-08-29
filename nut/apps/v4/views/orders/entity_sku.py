from apps.v4.views import APIJsonView, APIJsonSessionView
from apps.v4.models import APIEntity
from apps.v4.forms.entity_sku import CartForm

from apps.core.views import ErrorJsonResponse


class EntitySKUView(APIJsonView):

    http_method_names = ['get']

    def get_data(self, context):
        try:
            entity = APIEntity.objects.get(entity_hash = self.entity_hash)
        except APIEntity.DoesNotExist:
            raise
        print entity.skus.all()

        entity_res = entity.v4_toDict()
        sku_list   = list()
        for row in entity.skus.filter(status=1):
            sku_list.append(
                row.toDict(),
            )
        entity_res.update(
            {
                'skus': sku_list,
            }
        )

        return entity_res

    def get(self, request, *args, **kwargs):
        self.entity_hash = kwargs.pop('entity_hash', None)

        assert self.entity_hash is not None
        return super(EntitySKUView, self).get(request, *args, **kwargs)


class AddSKUToCartView(APIJsonSessionView):

    http_method_names = ['post']

    def get_data(self, context):
        form = CartForm(self.request.POST)
        if form.is_valid():
            form.save(user=self.session.user)
            return {'status': True}
        print form.errors
        return ErrorJsonResponse(status=401)

    # def post(self, request, *args, **kwargs):


        # return super(AddSKUToCartView, self).post(request, *args, **kwargs)
        # else:

            # return
