# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Note
from apps.core.utils.tag import TagParser
# from apps.notifications import notify

from apps.web.utils.formtools import innerStrip,clean_user_text

from django.utils.log import getLogger
from string import  maketrans
log = getLogger('django')


class NoteForm(forms.ModelForm):


    class Meta:
        model = Note
        fields = ('note', )
        label = {
            'note':_('content'),
        }
        widgets = {
            'note': forms.Textarea(attrs={'class':'form-control', 'style':"resize: none;", 'rows':'4', 'placeholder':u"写点评 ＃贴标签"}),
            # 'email': forms.TextInput(attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        self.entity_id = kwargs.pop('eid', None)
        self.user = kwargs.pop('user', None)
        self.note_id = kwargs.pop('nid', Note)
        super(NoteForm, self).__init__(*args, **kwargs)

    def clean_note(self):
        _note_text = self.cleaned_data.get('note')
        _note_text = innerStrip(_note_text)
        _note_text = clean_user_text(_note_text)
        _note_text = _note_text.replace(u"＃", "#")
        return _note_text

    def save(self, commit=True):
        # note = super(NoteForm, self).save(commit=commit)
        _note = self.cleaned_data.get('note')

        try:
            note = Note.objects.get(user=self.user, entity_id=self.entity_id)
        except Note.DoesNotExist:
            note = Note.objects.create(
                note=_note,
                user = self.user,
                entity_id = self.entity_id,
            )
        # except Note.MultipleObjectsReturned:
        # the following is deprecated implemention
        # should be removed in the future
        # t = TagParser(note.note)
        # t.create_tag(user_id=self.user.pk, entity_id=self.entity_id)

        return note


    def update(self):
        _note = self.cleaned_data.get('note')
        note = Note.objects.get(pk=self.note_id, user=self.user)
        note.note = _note
        note.save()
        t = TagParser(_note)
        if not self.entity_id :
            self.entity_id = note.entity_id

        t.create_tag(user_id=self.user.pk, entity_id=self.entity_id)
        return note
    #     _content = self.cleaned_data.get('content')
    #     log.info(_content)
    #
    #     note = Note.objects.create(
    #
    #     )
    #
    #     pass

__author__ = 'edison'
