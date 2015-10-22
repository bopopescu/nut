#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django.forms.widgets import SelectMultiple, \
    TextInput, URLInput, DateTimeInput, CheckboxInput, Textarea

from apps.core.models import EDM
from apps.core.utils.image import HandleImage


image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


class EDMDetailForm(ModelForm):
    class Meta:
        model = EDM
        fields = ('title', 'cover_image', 'cover_hype_link',
                  'cover_description', 'articles', 'approved',
                  'publish_time')
        widgets = {
            'approved': CheckboxInput(attrs={'class': ''}),
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

    def save(self, commit=True):
        cover_image = self.cleaned_data.get('cover_image')
        if self.instance.pk is None or self.instance.cover_image != cover_image:
            _image = HandleImage(cover_image)
            file_path = "%s%s.jpg" % (image_path, _image.name)
            self.instance.cover_image = file_path
            default_storage.save(file_path, ContentFile(_image.image_data))
        return super(EDMDetailForm, self).save()