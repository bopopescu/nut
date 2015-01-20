# coding=utf8
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

    def save(self):
        _note_text = self.cleaned_data.get('note')
        _user_id = self.cleaned_data.get('session')

        # log.info("user id %s" % _user_id)
        _note_text = _note_text.replace(u"＃", "#")

        note = Note(
            user_id = _user_id,
            entity = self.entity_cache,
        )
        note.note = _note_text
        note.save()

        return note.v3_toDict()


class UpdateNoteForms(forms.Form):

    note = forms.CharField(
        widget=forms.TextInput()
    )

    def __init__(self, note, *args, **kwargs):
        self.note_cache = note
        super(UpdateNoteForms, self).__init__(*args, **kwargs)

    def update(self):
        _note_text = self.cleaned_data.get('note')
        _note_text = _note_text.replace(u"＃", "#")

        # _user_id = self.cleaned_data.get('session')
        self.note_cache.note = _note_text
        self.note_cache.save()

        return self.note_cache.v3_toDict()



__author__ = 'edison'
