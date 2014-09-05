from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

from apps.core.models import Note

log = getLogger('django')


class NoteForm(forms.Form):

    note_id = forms.IntegerField(label=_('note_id'),
                                 widget=forms.NumberInput(attrs={'class':'form-control', 'readonly':''}),
                                 help_text=_(''))

    creator = forms.CharField(label=_('creator'),
                              widget=forms.TextInput(attrs={'class':'form-control', 'readonly':''}),
                              help_text=_(''))

    content = forms.CharField(label=_('content'),
                              widget=forms.Textarea(attrs={'class':'form-control'}),
                              help_text=_(''))

    post_time = forms.DateTimeField(label=_('post_time'),
                                    widget=forms.DateTimeInput(attrs={'class':'form-control', 'readonly':''}),
                                    help_text=_(''))

    updated_time = forms.DateTimeField(label=_('updated time'),
                                       widget=forms.DateTimeInput(attrs={'class':'form-control'}),
                                       help_text=_(''))

    def __init__(self, note, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.note = note
        self.fields['status'] = forms.ChoiceField(label=_('status'),
                                                  choices=Note.NOTE_STATUS_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control'}),
                                                  help_text=_(''))

    def save(self):
        _content = self.cleaned_data.get('content')
        _status = self.cleaned_data.get('status')
        self.note.note = _content
        self.note.status = _status
        self.note.save()


# class CreateNoteForm(forms.Form):
#     content = forms.CharField(
#         label=_('creator'),
#         widget=forms.Textarea(attrs={'class':'form-control' }),
#         help_text=_(''),
#     )





__author__ = 'edison'
