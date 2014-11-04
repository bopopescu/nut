from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger


log = getLogger('django')


class BaseArticleForms(forms.Form):

    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text = _(''),
    )

    content = forms.CharField(
        label=_('content'),
        widget=forms.Textarea(attrs={'class':'form-control', 'id':'summernote'}),
        help_text=_(''),
    )


class CreateArticleForms(BaseArticleForms):

    def save(self):
        pass


class EditArticleForms(BaseArticleForms):



    def save(self):

        pass



__author__ = 'edison'
