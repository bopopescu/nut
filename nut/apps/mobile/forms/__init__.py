from apps.mobile.models import LaunchBoard
from apps.core.utils.image import HandleImage

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
image_host = getattr(settings, 'IMAGE_HOST', None)


class LaunchBoardForm(forms.Form):
    YES_OR_NO = (
        (0, _('no')),
        (1, _('yes')),
    )
    # forms.EmailField
    launchImage = forms.FileField(widget=forms.FileInput(), required=False)
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

    def save(self):
        pass


class CreateLaunchBoardForm(LaunchBoardForm):

    def save(self):
        _image = self.cleaned_data.get('image')
        _title = self.cleaned_data.get('title')
        _description = self.cleaned_data.get('description')

        # if _image:
        launch_image =  HandleImage(_image)
        image_name = image_path + "%s.jpg" % launch_image.name
        launch = LaunchBoard()
        launch.launchImage = image_name
        launch.title = _title
        launch.description = _description
        launch.save()


class EditLaunchBoardForm(LaunchBoardForm):

    def save(self):
        pass

__author__ = 'edison7500'
