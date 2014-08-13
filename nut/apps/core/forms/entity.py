from django import forms
from django.utils.translation import gettext_lazy as _


class EntityFrom(forms.Form):
    id = forms.CharField(label=_('user_id'),
                         widget=forms.NumberInput(attrs={'class':'form-control', 'readonly':''}),
                         help_text=_(''))
    brand = forms.CharField(label=_('brand'),
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            required=False,
                            help_text=_(''))
    title = forms.CharField(label=_('title'),
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            help_text=_(''))
    intro = forms.CharField(label=_('intro'), widget=forms.Textarea(attrs={'class':'form-control'}),
                            required=False,
                            help_text=_(''))
    price = forms.DecimalField(max_digits=20, decimal_places=2,
                               label=_('price'),
                               widget=forms.NumberInput(attrs={'class':'form-control'}),
                               help_text=_(''))


__author__ = 'edison7500'
