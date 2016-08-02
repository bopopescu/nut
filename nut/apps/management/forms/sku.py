# encoding: utf-8
import json

from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, HiddenInput
from apps.core.models import SKU, Entity


class SKUForm(ModelForm):

    entity = CharField()
    attrs = CharField()

    def clean_entity(self):
        entity_id = self.cleaned_data['entity']
        return Entity.objects.get(id=entity_id)

    def clean_attrs(self):
        attrs = json.loads(self.cleaned_data['attrs'])
        entity = self.cleaned_data['entity']
        attrs_list = [s.attrs for s in entity.skus.all()]
        if attrs == {}:
            attrs = u''
        if attrs in attrs_list:
            raise ValidationError("属性已存在")
        return attrs

    def __init__(self, *args, **kwargs):
        super(SKUForm, self).__init__(*args, **kwargs)
        for key , field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

        self.fields['entity'].widget.attrs['readonly'] = True
        self.fields['attrs'].widget = HiddenInput()

    def save(self, commit=False):
        instance = super(SKUForm, self).save(commit=commit)
        instance.attrs = self.cleaned_data['attrs']
        instance.save()

    class Meta:
        model = SKU
        fields = [ 'stock', 'origin_price', 'promo_price', 'status', 'entity', 'attrs']


