from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

log = getLogger('django')

from apps.core.models import Banner, Show_Banner

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
                                                  help_text=_(''))


class CreateBannerForm(BaseBannerForm):


    content_type = forms.ChoiceField(
                                    label=_('content_type'),
                                    choices=Banner.CONTENT_TYPE_CHOICES,
                                    widget=forms.Select(attrs={'class':'form-control'}),
                                    help_text=_(''),
                                )
    key = forms.CharField(label=_('key'),
                          widget=forms.TextInput(attrs={'class':'form-control'}),
                          help_text=_(''))
    banner_image = forms.ImageField(
                        label=_('banner image'),
                        widget=forms.FileInput(attrs={'class':'controls'}),
                        # required=False,
                        help_text=_(''),
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
    #                                               help_text=_(''))


    def save(self):
        banner_image = self.cleaned_data['banner_image']

        log.info(banner_image)


class EditBannerForm(BaseBannerForm):
    # content_type = forms.ChoiceField(label=_('content_type'),
    #                                 choices=Banner.CONTENT_TYPE_CHOICES,
    #                                widget=forms.Select(attrs={'class':'form-control', 'readonly':''}),
    #                                help_text=_(''))
    # key = forms.CharField(label=_('key'),
    #                       widget=forms.TextInput(attrs={'class':'form-control', 'readonly':''}),
    #                       help_text=_(''))
    banner_image = forms.ImageField(
                                    label=_('banner image'),
                                    widget=forms.FileInput(attrs={'class':'controls'}),
                                    required=False,
                                    help_text=_(''),
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
                                                  help_text=_(''))

    def clean_position(self):
        _position = self.cleaned_data.get('position')
        return int(_position)

    def save(self):
        banner_image = self.cleaned_data['banner_image']
        position = self.clean_position()
        if position > 0 and self.banner.position == 0:
            show = Show_Banner.objects.get(pk= position)
            show.banner = self.banner
            show.save()
        elif self.banner.position != position:
            show = Show_Banner.objects.get(pk = position)
            tmp_show = Show_Banner.objects.get(pk = self.banner.position)
            tmp_banner = show.banner
            show.banner = self.banner
            tmp_show.banner = tmp_banner
            show.save()
            tmp_show.save()

__author__ = 'edison'
