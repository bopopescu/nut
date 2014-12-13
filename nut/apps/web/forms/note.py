# coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.log import getLogger

from apps.core.models import Note


class NoteForm(forms.Form):

    content = forms.CharField(
        label=_('content'),
        widget=forms.Textarea(
            attrs={'class':'form-control', 'style':"resize: none;", 'rows':'4', 'placeholder':u"写点评 ＃贴标签"}
        )
    )


    def save(self):

        pass

__author__ = 'edison'
