from django import forms
from django.utils.translation import gettext_lazy as _
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
#
# from apps.core.utils.image import HandleImage
#
# from django.conf import settings
#
# image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


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


__author__ = 'edison'
