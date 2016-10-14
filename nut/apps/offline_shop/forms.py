import json

from django.forms import ModelForm
from django import forms
from django.shortcuts import get_object_or_404

from apps.core.models import GKUser
from apps.offline_shop.models import Offline_Shop_Info


class OfflineShopInfoForm(ModelForm):
    images = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(OfflineShopInfoForm, self).__init__(*args, **kwargs)
        for fieldkey, field in self.fields.iteritems():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images is None or len(images) == 0:
            return []
        else:
            images = json.loads(images)
            if isinstance(images, list):
                return images
            else:
                raise



    class Meta:
        model = Offline_Shop_Info
        fields = [
                  'shop_name',
                  'shop_tel',
                  'shop_mobile',
                  'shop_desc',
                  'shop_address',
                  'address_lng',
                  'address_lat',
                  'images',
                  ]