from django import forms
from apps.core.forms.brand import BrandForm
# from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.core.models import Brand
from apps.core.utils.image import HandleImage

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


class EditBrandForm(BrandForm):

    def __init__(self, brand, *args, **kwargs):
        self.brand_cache = brand
        super(EditBrandForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        _name = self.cleaned_data.get('name')
        _name = _name.strip(' \t\n\r')

        if self.brand_cache.name.lower() == _name.lower():
            return _name

        try:
            Brand.objects.get(name=_name)
        except Brand.DoesNotExist:
            return _name

        raise forms.ValidationError(
            self.error_messages['duplicate_brand_name'],
            code='duplicate_brand_name',
        )

    def save(self):
        _name = self.cleaned_data.get('name')
        _alias = self.cleaned_data.get('alias')
        _national = self.cleaned_data.get('national')
        _company = self.cleaned_data.get('company')
        _website = self.cleaned_data.get('website')
        _tmall_link =self.cleaned_data.get('tmall_link')
        _intro = self.cleaned_data.get('intro')
        _icon_file = self.cleaned_data.get('icon')
        _status = self.cleaned_data.get('status')

        self.brand_cache.name = _name
        self.brand_cache.alias = _alias
        self.brand_cache.national = _national
        self.brand_cache.company = _company
        self.brand_cache.website = _website
        self.brand_cache.tmall_link = _tmall_link
        self.brand_cache.status = _status

        if _intro:
            self.brand_cache.intro = _intro

        if _icon_file:
            _image = HandleImage(_icon_file)
            file_path = "%s%s.jpg" % (image_path, _image.name)
            default_storage.save(file_path, ContentFile(_image.image_data))
            # self.banner.image = file_path
            self.brand_cache.icon = file_path

        self.brand_cache.save()

        return self.brand_cache


class CreateBrandForm(BrandForm):

    def __init__(self, *args, **kwargs):
        super(CreateBrandForm, self).__init__(*args, **kwargs)

    def save(self):
        _name = self.cleaned_data.get('name')
        _alias = self.cleaned_data.get('alias')
        _national = self.cleaned_data.get('national')
        _company = self.cleaned_data.get('company')
        _website = self.cleaned_data.get('website')
        _tmall_link =self.cleaned_data.get('tmall_link')
        _intro = self.cleaned_data.get('intro')
        _icon_file = self.cleaned_data.get('icon')
        _status = self.cleaned_data.get('status')

        brand = Brand()
        brand.name = _name
        brand.alias = _alias
        brand.national = _national
        brand.company = _company
        brand.website = _website
        brand.tmall_link = _tmall_link

        if _intro:
            brand.intro = _intro

        if _icon_file:
            _image = HandleImage(_icon_file)
            file_path = "%s%s.jpg" % (image_path, _image.name)
            default_storage.save(file_path, ContentFile(_image.image_data))
            # self.banner.image = file_path
            brand.icon = file_path
        # brand.intro = _intro

        brand.status = _status
        brand.save()
        return brand


__author__ = 'edison'
