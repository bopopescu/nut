from django import forms
from apps.v4.models import APIJpush

class PushForm(forms.Form):
    rid = forms.CharField(
        widget=forms.TextInput(),
    )

    model = forms.CharField(
        widget=forms.TextInput(),
    )

    version = forms.CharField(
        widget=forms.TextInput(),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PushForm, self).__init__(*args, **kwargs)

    def save(self):
        _rid = self.cleaned_data.get('rid')
        _model = self.cleaned_data.get('model')
        _version = self.cleaned_data.get('version')

        try:
            self.push =  APIJpush.objects.get(rid=_rid)
        except APIJpush.DoesNotExist:
            self.push = APIJpush()
            self.push.rid = _rid
        finally:
            self.push.user = self.user
            self.push.model = _model
            self.push.version = _version
            self.push.save()
    # def update(self):

__author__ = 'edison7500'
