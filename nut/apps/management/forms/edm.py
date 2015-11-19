#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.db.models import Q
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django.forms.widgets import SelectMultiple
from django.forms.widgets import TextInput
from django.forms.widgets import URLInput
from django.forms.widgets import DateTimeInput
from django.forms.widgets import Textarea
from datetime import datetime, timedelta

from apps.core.models import EDM, Selection_Article
from apps.core.utils.image import HandleImage


image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


class EDMDetailForm(ModelForm):
    class Meta:
        model = EDM
        fields = ('title', 'cover_image', 'cover_hype_link',
                  'cover_description', 'selection_articles', 'publish_time')
        widgets = {
            'publish_time': DateTimeInput(attrs={'class': 'form-control'}),
            'cover_description': Textarea(attrs={'class': 'form-control'}),
            'selection_articles': SelectMultiple(
                attrs={'class': 'chosen-select'}),
            'title': TextInput(attrs={'class': 'form-control'}),
            'cover_hype_link': URLInput(attrs={'class': 'form-control'})
        }
        labels = {'title': _('title'), 'cover_image': _('cover image'),
                  'cover_hype_link': _('cover hype link'),
                  'cover_description': _('cover description'),
                  'selection_articles': _('selection articles'),
                  'publish_time': _('publish time')}

    cover_image = forms.ImageField(
        label=_('Select an Image'),
        help_text=_('max. 2 megabytes'),
    )

    def __init__(self, *args, **kwargs):
        super(EDMDetailForm, self).__init__(*args, **kwargs)
        now = datetime.now()
        amonth_ago = now - timedelta(days=32)
        article_filter_q = [Q(is_published=True) & Q(pub_time__gte=amonth_ago)
                            & Q(pub_time__lte=now)]
        if 'fields' in self:
            article_filter_q = (
                article_filter_q | Q(pk__in=self.initial['selection_articles']))
            self.fields['selection_articles'].queryset = \
                Selection_Article.objects.filter(*article_filter_q)
        else:
            self.base_fields['selection_articles'].queryset = \
                Selection_Article.objects.filter(*article_filter_q)

    def save(self, commit=True):
        cover_image = self.cleaned_data.get('cover_image')
        if self.instance.pk is None or self.instance.cover_image != cover_image:
            _image = HandleImage(cover_image)
            file_path = "%s%s.jpg" % (image_path, _image.name)
            self.instance.cover_image = file_path
            default_storage.save(file_path, ContentFile(_image.image_data))
        if self.has_changed():
            self.instance.status = EDM.waiting_for_sd_verify
        return super(EDMDetailForm, self).save()
