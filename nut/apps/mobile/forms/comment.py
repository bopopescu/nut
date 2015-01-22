from django import forms
from apps.mobile.models import Session_Key
from apps.core.models import Note_Comment

from apps.notifications import notify

class PostNoteCommentForm(forms.Form):
    session = forms.CharField(
        widget=forms.TextInput()
    )
    comment = forms.CharField(
        widget=forms.TextInput()
    )
    reply_to_comment = forms.IntegerField(
        widget=forms.TextInput(),
        required=False,
    )
    reply_to_user_id = forms.IntegerField(
        widget=forms.TextInput(),
        required=False
    )

    def __init__(self, note, *args, **kwargs):
        self.note_cache = note
        super(PostNoteCommentForm, self).__init__(*args, **kwargs)


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
        _comment_text = self.cleaned_data.get('comment')
        _reply_to_comment = self.cleaned_data.get('reply_to_comment')
        _reply_to_user_id = self.cleaned_data.get('reply_to_user_id')
        _user_id = self.cleaned_data.get('session')


        note_comment = Note_Comment(
            note = self.note_cache,
            user_id = _user_id,
            content = _comment_text,
        )

        if _reply_to_user_id:
            note_comment.replied_user_id = _reply_to_user_id
            note_comment.replied_comment_id = _reply_to_comment

        note_comment.save()
        notify.send(note_comment.user, recipient=self.note_cache.user, verb="replied", action_object=note_comment)
        return note_comment.v3_toDict()

__author__ = 'edison'
