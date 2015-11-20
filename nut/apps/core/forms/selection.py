from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from apps.core.tasks.selection import set_publish_time



class SelectionForm(forms.Form):
    YES_OR_NO = (
        (1, _('yes')),
        (0, _('no')),
    )

    pub_time = forms.DateTimeField(
        label=_('publish datetime'),
        widget=forms.DateTimeInput(attrs={'class':'form-control'}),

        initial=datetime.now()
    )

    is_published = forms.ChoiceField(
        label=_('is_published'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),

        initial=1,
    )

    def __init__(self, selection, *args, **kwargs):
        self.selection = selection
        super(SelectionForm, self).__init__(*args, **kwargs)

    def update(self):
        _pub_time = self.cleaned_data.get('pub_time')
        _is_published = self.cleaned_data.get('is_published')

        _is_published = int(_is_published)

        self.selection.pub_time = _pub_time
        self.selection.is_published = _is_published
        self.selection.save()

        return self.selection



class SetPublishDatetimeForm(forms.Form):

    publish_number = forms.IntegerField(
        label=_('publish number'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('default number'),
        initial=91,
    )

    interval_time = forms.IntegerField(
        label=_('interval time'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('this value is second'),
        initial=600,
    )

    start_time = forms.DateTimeField(
        label=_('start time'),
        widget=forms.DateTimeInput(attrs={'class':'form-control'}),
        help_text=_('set selection entity publish begin time'),
        initial=datetime.now(),
    )

    def save(self):
        _publish_number = self.cleaned_data.get('publish_number')
        _start_time = self.cleaned_data.get('start_time')
        _interval_time = self.cleaned_data.get('interval_time')

        _start_time = _start_time.strftime("%Y-%m-%d %H:%M:%S")

        set_publish_time.delay(publish_number=_publish_number,
                         start_time=_start_time,
                         interval_time=_interval_time)


__author__ = 'edison7500'
