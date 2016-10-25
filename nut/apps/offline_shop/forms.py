import json

from django.forms import ModelForm
from django import forms
from django.shortcuts import get_object_or_404

from apps.core.models import GKUser
from apps.offline_shop.models import Offline_Shop_Info


class OfflineShopInfoForm(ModelForm):
    images = forms.CharField(required=False)
    status = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(OfflineShopInfoForm, self).__init__(*args, **kwargs)
        for fieldkey, field in self.fields.iteritems():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': ''})
        self.fields['images'].widget.attrs.update({'class': 'hidden'})
        self.fields['address_lng'].widget.attrs.update({'class': 'hidden'})
        self.fields['address_lat'].widget.attrs.update({'class': 'hidden'})

        if self.instance.images is None:
            self.fields['images'].initial = ''
        else:
            self.fields['images'].initial = json.dumps(self.instance.images)

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

    def save(self, *args, **kwargs):
        instance = super(OfflineShopInfoForm, self).save()
        instance.images = self.cleaned_data.get('images')
        instance.save()
        return instance


    class Meta:
        model = Offline_Shop_Info
        fields = [
                  'shop_name',
                  'shop_tel',
                  'shop_mobile',
                  'shop_desc',
                  'shop_address',
                  'shop_opentime',
                  'address_lng',
                  'address_lat',
                  'images',
                  'status',
                  'position'
                  ]