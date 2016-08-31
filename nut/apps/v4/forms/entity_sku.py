from django import forms
from apps.order.models import SKU
from apps.order.manager.cart import CartException


class CartForm(forms.Form):

    sid             = forms.IntegerField(
                        widget=forms.NumberInput(),
                    )
    volume          = forms.IntegerField(
                        widget=forms.NumberInput(), initial=1,
                        required=False,
                    )

    def clean_sid(self):
        sku_id      = self.cleaned_data.get('sid', None)

        assert  sku_id is not None

        try:
            sku     = SKU.objects.get(pk = sku_id)
            return sku
        except SKU.DoesNotExist as e:

            raise forms.ValidationError(
                e.message
            )

    def clean_volume(self):
        volume = self.cleaned_data.get('volume')
        if volume is None:
            volume = 1
        return volume

    def save(self, user):
        sku_id      = self.cleaned_data.get('sid')
        volume      = self.cleaned_data.get('volume')
        # print type(volume)
        try:
            cart_item = user.add_sku_to_cart(sku_id, volume)
        except CartException as e:
            raise forms.ValidationError(
                e.message
            )
        return cart_item


class DescCartItemForm(CartForm):

    def save(self, user):
        sku_id      = self.cleaned_data.get('sid')
        try:
            cart_item = user.decr_sku_in_cart(sku_id)
        except CartException as e:
            raise forms.ValidationError(
                e.message
            )
        return cart_item