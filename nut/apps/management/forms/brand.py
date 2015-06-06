from django import forms
from apps.core.forms.brand import BrandForm
# from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.core.utils.image import HandleImage

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


class EditBrandForm(BrandForm):

    def __init__(self, brand, *args, **kwargs):
        self.brand_cache = brand
        super(EditBrandForm, self).__init__(*args, **kwargs)

    def save(self):
        _name = self.cleaned_data.get('name')
        _national = self.cleaned_data.get('national')
        _company = self.cleaned_data.get('company')
        _website = self.cleaned_data.get('website')
        _intro = self.cleaned_data.get('intro')
        _icon_file = self.cleaned_data.get('icon')

        self.brand_cache.name = _name
        self.brand_cache.national = _national
        self.brand_cache.company = _company
        self.brand_cache.website = _website

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
        pass

__author__ = 'edison'
