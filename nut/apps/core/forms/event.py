from django import forms
from django.utils.translation import gettext_lazy as _
from apps.core.models import Event, Event_Status
from apps.tag.models import Tags
from django.utils.log import getLogger

log = getLogger('django')


class BaseEventForm(forms.Form):
    YES_OR_NO = (
        (0, _('no')),
        (1, _('yes')),
    )

    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),

    )

    tag = forms.CharField(
        label=_('tag'),
        widget=forms.TextInput(attrs={'class':'form-control'}),

    )

    slug = forms.CharField(
        label=_('slug'),
        widget=forms.TextInput(attrs={'class':'form-control'}),

    )
    # change widget to textInput by An , explain later .
    status = forms.ChoiceField(
        label=_('is_on_top'),
        choices=YES_OR_NO,
        widget=forms.TextInput( attrs={'class':'form-control'}, ),
        required=False,

        initial=0,
    )

    is_published = forms.ChoiceField(
        label=_('is_published'),
        choices=YES_OR_NO,
        widget=forms.Select( attrs={'class':'form-control'}),
        required=False,
        help_text=_('is the event published ?'),
    )

    is_top = forms.ChoiceField(
        label=_('is_event_on_top'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
        required=False,
        help_text=_('is the event on top ? ')
    )

    def clean_tag(self):
        _tag = self.cleaned_data.get('tag')

        try:
            Tags.objects.get(name=_tag)
        except Tags.DoesNotExist:
            raise forms.ValidationError(
                _('tag is not exist'),
            )
        return _tag

    def clean_status(self):
        _status = self.cleaned_data.get('status')
        return int(_status)

    def clean_is_published(self):
        _is_published = self.cleaned_data.get('is_published')
        return int(_is_published)

    def clean_is_top(self):
        _is_top = self.cleaned_data.get('is_top')
        return int(_is_top)


class CreateEventForm(BaseEventForm):

    def save(self):
        _title = self.cleaned_data.get('title')
        _tag = self.cleaned_data.get('tag')
        _slug = self.cleaned_data.get('slug')
        _status = self.cleaned_data.get('status')
        _is_top = self.cleaned_data.get('is_top')
        _is_published = self.cleaned_data.get('is_published')
        # replace _status with _is_top
        _status = _is_top

        log.info(_status)

        if _status:
            Event.objects.all().update(status = False)
            Event_Status.objects.all().update(is_top=False)
        # only one Event_status can have is_top=True ATTR, SO DOES Event


        event = Event.objects.create(
            title = _title,
            tag = _tag,
            slug = _slug,
            status = _status,
        )
        event_status = Event_Status(event=event, is_published=_is_published, is_top=_is_top)
        event_status.save()

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
        # _status = int(_status)

        _is_published = self.cleaned_data.get('is_published',False)
        _is_published = int(_is_published)

        _is_top = self.cleaned_data.get('is_top',False)
        _is_top = int(_is_top)

        _status = _is_top

        if _status:
            Event.objects.all().update(status = False)
            Event_Status.objects.all().update(is_top=False)

        self.event.title = _title
        self.event.tag = _tag
        self.event.slug = _slug
        self.event.status = _status
        self.event.event_status.is_published = _is_published
        self.event.event_status.is_top = _is_top
        self.event.event_status.save()
        self.event.save()


__author__ = 'edison'
