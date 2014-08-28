from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

log = getLogger('django')


class CreateBannerForm(forms.Form):
    key = forms.CharField(label=_('key'))
    banner_image = forms.ImageField()

__author__ = 'edison'
