from django import forms
from django.utils.translation import gettext_lazy as _
from apps.core.models import Event, Tag
# from base.models import Event, Tag



class BaseEventForm(forms.Form):
    YES_OR_NO = (
        (0, _('no')),
        (1, _('yes')),
    )
    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )

    tag = forms.CharField(
        label=_('tag'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('')
    )

    slug = forms.CharField(
        label=_('slug'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )

    status = forms.ChoiceField(
        label=_('status'),
        choices=YES_OR_NO,
        widget=forms.Select( attrs={'class':'form-control'}),
        required=False,
        help_text=_(''),
    )

    def clean_tag(self):
        _tag = self.cleaned_data.get('tag')

        try:
            Tag.objects.get(tag_hash=_tag)
        except Tag.DoesNotExist:
            raise forms.ValidationError(
                _('tag is not exist'),
            )
        return _tag


class CreateEventForm(BaseEventForm):

    def save(self):
        _title = self.cleaned_data.get('title')
        _tag = self.cleaned_data.get('tag')
        _slug = self.cleaned_data.get('slug')
        _status = self.cleaned_data.get('status', False)
        _status = int(_status)

        if _status:
            Event.objects.all().update(status = False)

        event = Event.objects.create(
            title = _title,
            tag = _tag,
            slug = _slug,
            status = _status,
        )

        return event



class EditEventForm(BaseEventForm):


    def __init__(self, event, *args, **kwargs):
        self.event = event
        super(EditEventForm, self).__init__(*args, **kwargs)


    def save(self):
        _title = self.cleaned_data.get('title')
        _tag = self.cleaned_data.get('tag')
        _slug = self.cleaned_data.get('slug')
        _status = self.cleaned_data.get('status', False)
        _status = int(_status)
        if _status:
            Event.objects.all().update(status = False)

        self.event.title = _title
        self.event.tag = _tag
        self.event.slug = _slug
        self.event.status = _status
        self.event.save()


__author__ = 'edison'
