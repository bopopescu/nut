from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.log import getLogger

log = getLogger('django')

from apps.core.utils.image import HandleImage
from apps.core.models import Banner, Show_Banner

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')

class BaseBannerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseBannerForm, self).__init__(*args, **kwargs)
        (none, first, second, third, fourth) = (0, 1, 2, 3, 4)
        BANNER_POSITION_CHOICES = (
            (none, _("none")),
            (first, _("first")),
            (second, _("second")),
            (third, _("third")),
            (fourth, _("fourth")),
        )
        self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                  choices=BANNER_POSITION_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control',}),
                                                  )

    def clean_position(self):
        _position = self.cleaned_data.get('position')
        return int(_position)


class CreateBannerForm(BaseBannerForm):


    content_type = forms.ChoiceField(
                                    label=_('content_type'),
                                    choices=Banner.CONTENT_TYPE_CHOICES,
                                    widget=forms.Select(attrs={'class':'form-control'}),

                                )
    key = forms.CharField(label=_('key'),
                          widget=forms.TextInput(attrs={'class':'form-control'}),
                          )
    banner_image = forms.ImageField(
                        label=_('banner image'),
                        widget=forms.FileInput(attrs={'class':'controls'}),
                        # required=False,

                    )


    # def __init__(self, *args, **kwargs):
    #     super(CreateBannerForm, self).__init__(*args, **kwargs)
    #     (none, first, second, third, fourth) = (0, 1, 2, 3, 4)
    #     BANNER_POSITION_CHOICES = (
    #         (none, _("none")),
    #         (first, _("first")),
    #         (second, _("second")),
    #         (third, _("third")),
    #         (fourth, _("fourth")),
    #     )
    #     self.fields['position'] = forms.ChoiceField(label=_('position'),
    #                                               choices=BANNER_POSITION_CHOICES,
    #                                               widget=forms.Select(attrs={'class':'form-control',}),
    #                                               )


    def save(self):
        content_type = self.cleaned_data.get('content_type')
        key = self.cleaned_data.get('key')
        banner_image = self.cleaned_data.get('banner_image')
        position = self.clean_position()

        # log.info(banner_image)
        _image = HandleImage(banner_image)
        file_path = "%s%s.jpg" % (image_path, _image.name)
        default_storage.save(file_path, ContentFile(_image.image_data))

        banner = Banner.objects.create(
            content_type = content_type,
            image = file_path,
            key = key,
            position = position,
        )

        if position > 0:
            try:
                show = Show_Banner.objects.get(pk = position)
                show.banner = banner
                show.save()
            except Show_Banner.DoesNotExist:
                Show_Banner.objects.create(
                    id = position,
                    banner = banner,
                )

        return banner

class EditBannerForm(BaseBannerForm):
    content_type = forms.ChoiceField(label=_('content_type'),
                                    choices=Banner.CONTENT_TYPE_CHOICES,
                                   widget=forms.Select(attrs={'class':'form-control'}),
                                   )
    key = forms.CharField(label=_('key'),
                          widget=forms.TextInput(attrs={'class':'form-control'}),
                          )
    banner_image = forms.ImageField(
                                    label=_('banner image'),
                                    widget=forms.FileInput(attrs={'class':'controls'}),
                                    required=False,

                                )

    def __init__(self, banner, *args, **kwargs):
        self.banner = banner
        super(EditBannerForm, self).__init__(*args, **kwargs)
        if self.banner.has_show_banner:
            (none, first, second, third, fourth) = (0, 1, 2, 3, 4)
            BANNER_POSITION_CHOICES = (
                # (none, _("none")),
                (first, _("first")),
                (second, _("second")),
                (third, _("third")),
                (fourth, _("fourth")),
            )
            self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                  choices=BANNER_POSITION_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control',}),
                                                  )

    def save(self):
        banner_image = self.cleaned_data.get('banner_image')
        position = self.clean_position()
        content_type = self.cleaned_data.get('content_type')
        key = self.cleaned_data.get('key')

        self.banner.key = key
        self.banner.content_type = content_type
        # self.banner.save()

        if banner_image:
            _image = HandleImage(banner_image)
            file_path = "%s%s.jpg" % (image_path, _image.name)
            default_storage.save(file_path, ContentFile(_image.image_data))
            self.banner.image = file_path
        self.banner.save()

        if position > 0 and self.banner.position == 0:
            try:
                show = Show_Banner.objects.get(pk= position)
                show.banner = self.banner
                show.save()
            except Show_Banner.DoesNotExist:
                Show_Banner.objects.create(
                    id = position,
                    banner = self.banner,
                )
        elif self.banner.position != position:
            show = Show_Banner.objects.get(pk = position)
            tmp_show = Show_Banner.objects.get(pk = self.banner.position)
            tmp_banner = show.banner
            show.banner = self.banner
            tmp_show.banner = tmp_banner
            show.save()
            tmp_show.save()

        return self.banner

__author__ = 'edison'
