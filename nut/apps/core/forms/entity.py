from django import forms
from django.utils.translation import gettext_lazy as _


class EntityFrom(forms.Form):
    id = forms.CharField()
    brand = forms.CharField()
    title = forms.CharField()
    intro = forms.CharField()
    price = forms.DecimalField(max_digits=20, decimal_places=2)


__author__ = 'edison7500'
