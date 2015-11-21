from apps.mobile.models import LaunchBoard
from apps.core.utils.image import HandleImage

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
image_host = getattr(settings, 'IMAGE_HOST', None)


class LaunchBoardForm(forms.Form):
    YES_OR_NO = (
        (0, _('no')),
        (1, _('yes')),
    )
    # forms.EmailField
    launchImage = forms.ImageField(widget=forms.FileInput(attrs={'class':'controls'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    action = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    status = forms.ChoiceField(
        label=_('enable'),
        choices=YES_OR_NO,
        widget=forms.Select( attrs={'class':'form-control'}, ),
        required=False,
        help_text=_(''),
        initial=0,
    )

    def clean_status(self):
        _status = self.cleaned_data.get('status')
        return int(_status)

    def save(self):
        pass


class CreateLaunchBoardForm(LaunchBoardForm):

    def save(self):
        _image = self.cleaned_data.get('launchImage')
        _title = self.cleaned_data.get('title')
        _description = self.cleaned_data.get('description')
        _action = self.cleaned_data.get('action')
        _status = self.cleaned_data.get('status')
        # print _image
        launch_image = HandleImage(_image)
        image_name = image_path + "%s.jpg" % launch_image.name
        default_storage.save(image_name, ContentFile(launch_image.image_data))
        launch = LaunchBoard()
        launch.launchImage = image_name
        launch.title = _title
        launch.description = _description
        launch.action = _action
        launch.status = _status
        launch.save()


class EditLaunchBoardForm(LaunchBoardForm):

    def save(self):
        _image = self.cleaned_data.get('launchImage')
        _title = self.cleaned_data.get('title')
        _description = self.cleaned_data.get('description')
        _action = self.cleaned_data.get('action')
        _status = self.cleaned_data.get('status')

__author__ = 'edison7500'
