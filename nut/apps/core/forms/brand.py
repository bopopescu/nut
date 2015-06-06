from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.core.utils.image import HandleImage

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


class BrandForm(forms.Form):

    icon = forms.FileField(
        label=_('icon'),
        widget=forms.FileInput(),
        required=False,
    )

    name = forms.CharField(
        label=_('brand name'),
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    national = forms.CharField(
        label=_('national'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        # required=False,
    )

    company = forms.CharField(
        label=_('company'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        # required=False,
    )

    website = forms.URLField(
        label=_('website'),
        widget=forms.URLInput(attrs={'class':'form-control'}),
        required=False,
    )

    intro = forms.CharField(
        label=_('intro'),
        widget=forms.Textarea(attrs={'class':'form-control'}),
        required=False,
    )
    #
    # def __init__(self, brand, *args, **kwargs):
    #     self.brand_cache = brand
    #     super(BrandForm, self).__init__(*args, **kwargs)

    def save(self):

        pass


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

__author__ = 'edison'
