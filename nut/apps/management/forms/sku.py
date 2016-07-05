from django.forms import ModelForm, CharField
from apps.core.models import SKU


class SKUForm(ModelForm):

    entity = CharField()
    attributes = CharField()

    def __init__(self, *args, **kwargs):
        super(SKUForm, self).__init__(*args, **kwargs)
        for key , field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

        self.fields['entity'].widget.attrs['readonly'] = True

    class Meta:
        model = SKU
        fields = [ 'stock', 'origin_price', 'promo_price', 'status', 'entity', 'attributes']


