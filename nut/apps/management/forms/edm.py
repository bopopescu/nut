#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from apps.core.models import EDM
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django.forms.widgets import SelectMultiple, \
    TextInput, URLInput, FileInput, DateTimeInput, CheckboxInput, Select, \
    Textarea


class EDMDetailForm(ModelForm):
    class Meta:
        model = EDM
        fields = ('title', 'cover_image', 'cover_hype_link',
                  'cover_description', 'articles', 'verification',
                  'publish_time')
        widgets = {
            'verification': CheckboxInput(attrs={'class': ''}),
            'publish_time': DateTimeInput(attrs={'class': 'form-control'}),
            'cover_description': Textarea(attrs={'class': 'form-control'}),
            'articles': SelectMultiple(attrs={'class': 'chosen-select'}),
            'title': TextInput(attrs={'class': 'form-control'}),
            'cover_hype_link': URLInput(attrs={'class': 'form-control'})
        }

    cover_image = forms.ImageField(
        label=_('Select an Image'),
        help_text=_('max. 2 megabytes'),
    )
