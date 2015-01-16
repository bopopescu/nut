from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

from apps.core.models import Note
from apps.core.models import GKUser
from apps.core.forms import get_admin_user_choices

log = getLogger('django')


# def get_admin_user_choices():
#     user_list = GKUser.objects.editor_or_admin()
#     res = map(lambda x: (x.pk, x.profile.nickname), user_list)
#     return res

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


class CreateNoteForm(forms.Form):
    YES_OR_NO = (
        (1, _('yes')),
        (0, _('no')),
    )

    content = forms.CharField(
        label=_('content'),
        widget=forms.Textarea(attrs={'class':'form-control' }),
        help_text=_(''),
    )

    is_top = forms.ChoiceField(
        label=_('is_top'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
        help_text=_(''),
        initial=False,
    )
    def __init__(self, entity, *args, **kwargs):
        self.entity_cache = entity
        super(CreateNoteForm, self).__init__(*args, **kwargs)

        user_choices = get_admin_user_choices()
        self.fields['user'] = forms.ChoiceField(
            label=_('user'),
            choices=user_choices,
            widget=forms.Select(attrs={'class':'form-control'}),
            help_text=_(''),
        )

    def save(self):

        _content = self.cleaned_data.get('content')
        _user_id = self.cleaned_data.get('user')
        _is_top = self.cleaned_data.get('is_top')
        _is_top = int(_is_top)

        log.info(_user_id)
        # if _is_top:
        #     pass
        try:
            user = GKUser.objects.get(pk = _user_id)
        except GKUser.DoesNotExist:
            raise


        try:
            note = Note.objects.get(user=user, entity=self.entity_cache)
            note.note = _content
            note.status = _is_top
            note.save()
        except Note.DoesNotExist:
            note = Note(
                entity = self.entity_cache,
                user = user,
                note = _content,
                status = _is_top,
            )
            note.save()
        # log.info(_content)

        return note


__author__ = 'edison'
