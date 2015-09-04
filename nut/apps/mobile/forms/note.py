# -*- coding: utf-8 -*-
from django import forms
from apps.core.models import Note
from apps.mobile.models import Session_Key


from django.utils.log import getLogger

log = getLogger('django')



class PostNoteForms(forms.Form):
    session = forms.CharField(
        widget=forms.TextInput()
    )
    note = forms.CharField(
        widget=forms.Textarea(),
    )

    def __init__(self, entity, *args, **kwargs):
        self.entity_cache = entity
        # self.user_cache = None
        super(PostNoteForms, self).__init__(*args, **kwargs)

    def clean_session(self):
        _key = self.cleaned_data.get('session')
        try:
            _session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist:
            raise forms.ValidationError(
                'user not login'
            )
        return _session.user_id


    def clean_note(self):
        _note_text = self.cleaned_data.get('note')
        _note_text = _note_text.replace(u"＃", "#")
        return _note_text

    def save(self):
        _note_text = self.cleaned_data.get('note')
        _user_id = self.cleaned_data.get('session')

        try:
            note = Note.objects.get(user_id=_user_id, entity=self.entity_cache)
        except Note.DoesNotExist:
            note = Note(
                user_id = _user_id,
                entity = self.entity_cache,
            )
            note.note = _note_text
            note.save()
            # notify.send(note.user, recipient=note.entity.user, action_object=note, verb='post note', target=note.entity)
        # t = TagParser(_note_text)
        # t.create_tag(user_id=_user_id, entity_id=self.entity_cache.pk)

        return note.v3_toDict()


class UpdateNoteForms(forms.Form):

    note = forms.CharField(
        widget=forms.TextInput()
    )

    def __init__(self, note, *args, **kwargs):
        self.note_cache = note
        super(UpdateNoteForms, self).__init__(*args, **kwargs)

    def clean_note(self):
        _note_text = self.cleaned_data.get('note')
        _note_text = _note_text.replace(u"＃", "#")
        return _note_text

    def update(self):
        _note_text = self.cleaned_data.get('note')
        # _note_text = _note_text.replace(u"＃", "#")

        # _user_id = self.cleaned_data.get('session')
        self.note_cache.note = _note_text
        self.note_cache.save()
        # t = TagParser(_note_text)
        # t.create_tag(user_id=self.note_cache.user_id, entity_id=self.note_cache.entity_id)

        return self.note_cache.v4_toDict()



__author__ = 'edison'
