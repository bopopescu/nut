from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

log = getLogger('django')

from apps.core.models import Banner


class CreateBannerForm(forms.Form):
    content_type = forms.ChoiceField(label=_('content_type'),
                                    choices=Banner.CONTENT_TYPE_CHOICES,
                                   widget=forms.Select(attrs={'class':'form-control'}),
                                   help_text=_(''))
    key = forms.CharField(label=_('key'),
                          widget=forms.TextInput(attrs={'class':'form-control'}),
                          help_text=_(''))
    banner_image = forms.ImageField(widget=forms.FileInput(attrs={'class':'controls'}))


    def save(self):
        banner_image = self.cleaned_data['banner_image']

        log.info(banner_image)



class EditBannerForm(forms.Form):
    content_type = forms.ChoiceField(label=_('content_type'),
                                    choices=Banner.CONTENT_TYPE_CHOICES,
                                   widget=forms.Select(attrs={'class':'form-control'}),
                                   help_text=_(''))
    key = forms.CharField(label=_('key'),
                          widget=forms.TextInput(attrs={'class':'form-control'}),
                          help_text=_(''))
    banner_image = forms.ImageField(widget=forms.FileInput(attrs={'class':'controls'}))

    def __init__(self, banner, *args, **kwargs):
        self.banner = banner
        super(EditBannerForm, self).__init__(*args, **kwargs)

    def save(self):
        pass

__author__ = 'edison'
