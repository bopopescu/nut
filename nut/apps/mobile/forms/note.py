from django import forms
from apps.core.models import Note
from apps.mobile.models import Session_Key

class PostNoteForms(forms.Form):
    session = forms.CharField(
        widget=forms.TextInput()
    )
    note = forms.CharField(
        widget=forms.TextInput(),
    )

    def __init__(self, entity, *args, **kwargs):
        self.entity_cache = entity
        self.user_cache = None
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




__author__ = 'edison'
