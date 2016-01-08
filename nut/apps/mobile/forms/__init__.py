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
    launchImage = forms.ImageField(widget=forms.FileInput(attrs={'class':'controls'}), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    device = forms.ChoiceField(label=_('device'),
                               choices=LaunchBoard.DEVICE_TYPE,
                               widget=forms.Select(attrs={'class':'form-control'}),
                               initial=LaunchBoard.all,
                               help_text=_(''))
    version = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    action_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
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

    def clean_device(self):
        _device = self.cleaned_data.get('device')
        return int(_device)

    def save(self):
        pass


class CreateLaunchBoardForm(LaunchBoardForm):

    def save(self):
        _image = self.cleaned_data.get('launchImage')
        _title = self.cleaned_data.get('title')
        _description = self.cleaned_data.get('description')
        _device = self.cleaned_data.get('device')
        _version = self.cleaned_data.get('version')
        _action_title = self.cleaned_data.get('action_title')
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
        launch.device = _device
        launch.version = _version
        launch.action_title = _action_title
        launch.action = _action
        launch.status = _status
        launch.save()


class EditLaunchBoardForm(LaunchBoardForm):


    def __init__(self, launch, *args, **kwargs):
        self.launch = launch
        super(EditLaunchBoardForm, self).__init__(*args, **kwargs)

    def save(self):
        _image = self.cleaned_data.get('launchImage', None)
        _title = self.cleaned_data.get('title')
        _description = self.cleaned_data.get('description')
        _device = self.cleaned_data.get('device')
        _version = self.cleaned_data.get('version')
        _action_title = self.cleaned_data.get('action_title')
        _action = self.cleaned_data.get('action')
        _status = self.cleaned_data.get('status')

        if _image:
            launch_image = HandleImage(_image)
            image_name = image_path + "%s.jpg" % launch_image.name
            default_storage.save(image_name, ContentFile(launch_image.image_data))
            self.launch.launchImage = image_name

        if _status:
            LaunchBoard.objects.filter(status=True).update(status = False)

        self.launch.title = _title
        self.launch.description = _description
        self.launch.action_title = _action_title
        self.launch.device = _device
        self.version = _version
        self.launch.action = _action
        self.launch.status = _status
        self.launch.save()

__author__ = 'edison7500'
