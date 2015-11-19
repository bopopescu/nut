from django import forms
from django.utils.translation import gettext_lazy as _
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
from django.utils.log import getLogger

from apps.core.utils.image import HandleImage
from apps.core.models import Show_Event_Banner, Event_Banner, Event

log = getLogger('django')

# from django.conf import settings
# image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
#

class BaseEventBannerForm(forms.Form):

    link = forms.URLField(
        label=_('link'),
        widget=forms.TextInput(attrs={'class':'form-control'}),

        required=False
    )
    event_banner_image = forms.FileField(
        label=_('event banner image'),
        widget=forms.FileInput(attrs={'class':'controls'}),

        required=True,
    )

    user_id = forms.CharField(
        label=_('taobao user id'),
        widget=forms.TextInput(attrs={'class':'form-control'}),

        required=False,
    )

    event_banner_background_image=forms.FileField(
        label=_('event banner background image'),
        widget=forms.FileInput(attrs={'class':'controls'}),

        required=False,
    )

    event_banner_background_color = forms.CharField(
        label=_('event banner background color'),
        widget=forms.TextInput(attrs={'class':'form-control'}),

        required=False,
    )


    def __init__(self, *args, **kwargs):
        super(BaseEventBannerForm, self).__init__(*args, **kwargs)

        self.fields['banner_type'] = forms.ChoiceField(
            label= _('banner type'),
            choices=Event_Banner.BANNER_TYPE__CHOICES,
            widget=forms.Select(attrs={'class':'form-control'}),

        )
        # (none, first, second, third, fourth, fifth) = (0, 1, 2, 3, 4, 5)
        # BANNER_POSITION_CHOICES = (
        #     (none, _("none")),
        #     (first, _("first")),
        #     (second, _("second")),
        #     (third, _("third")),
        #     (fourth, _("fourth")),
        #     (fifth, _("fifth")),
        # )
        # self.fields['position'] = forms.ChoiceField(label=_('position'),
        #                                           choices=BANNER_POSITION_CHOICES,
        #                                           widget=forms.Select(attrs={'class':'form-control',}),
        #                                           )


        events = Event.objects.all()
        events_list = list()
        for event in events:
            events_list.append((event.id, event.slug))
        events_choices = tuple(events_list)
        # Event_CHOICES = (
        #     (none, _("---------------------------")),
        # )
        events_choices = tuple([(None, '-------------')]) + events_choices
        self.fields['event'] = forms.ChoiceField(
            label=_('event'),
            choices=events_choices,
            widget=forms.Select(attrs={'class':'form-control',}),

            required=False
        )
    #
    def clean_position(self):
        _position = self.cleaned_data.get('position', 0)
        return int(_position)


class CreateEventBannerForms(BaseEventBannerForm):
    #
    # link = forms.URLField(
    #     label=_('link'),
    #     widget=forms.TextInput(attrs={'class':'form-control'}),
    #
    # )
    # event_banner_image = forms.FileField(
    #     label=_('event banner image'),
    #     widget=forms.FileInput(attrs={'class':'controls'}),
    #
    # )

    def save(self):
        link = self.cleaned_data.get('link')
        event_banner_image = self.cleaned_data.get('event_banner_image')
        event_banner_background_image = self.cleaned_data.get('event_banner_background_image',None)
        event_banner_background_color = self.cleaned_data.get('event_banner_background_color','fff')
        position = self.cleaned_data.get('position')
        banner_type = self.cleaned_data.get('banner_type')
        user_id = self.cleaned_data.get('user_id')


        # log.info(event_banner_image)
        _image = HandleImage(event_banner_image)
        # file_path = "%s%s.jpg" % (image_path, _image.name)
        # default_storage.save(file_path, ContentFile(_image.image_data))
        # log.info(f)
        #
        filename = _image.save()
        _background_image_file_name = None
        if event_banner_background_image:
            _background_image = HandleImage(event_banner_background_image)
            _background_image_file_name = _background_image.save()


        _event_banner = Event_Banner.objects.create(
            link = link,
            image = filename,
            banner_type = banner_type,
            user_id = user_id,
            background_image = _background_image_file_name,
            background_color = event_banner_background_color
        )
        #
        # if position > 0:
        #     try:
        #         show = Show_Event_Banner.objects.get(pk = position)
        #         show.banner = _event_banner
        #         show.save()
        #     except Show_Event_Banner.DoesNotExist:
        #         Show_Event_Banner.objects.create(
        #             banner = _event_banner
        #         )
        return _event_banner


class EditEventBannerForms(BaseEventBannerForm):
    
    event_banner_image = forms.FileField(
        label=_('event banner image'),
        widget=forms.FileInput(attrs={'class':'controls'}),

        required=False,
    )


    def __init__(self, banner, *args, **kwargs):
        self.banner = banner
        super(EditEventBannerForms, self).__init__(*args, **kwargs)
        log.info(kwargs)


        if self.banner.event:
            try:
                # event_id = kwargs['data']['event']
                positions = Show_Event_Banner.objects.filter(event = self.banner.event).count()
                position_list = list()
                for position in xrange(1, positions +1):
                    position_list.append((position, str(position)))
                position_choices = tuple(position_list)
                position_choices = tuple([(0, '-------------')]) + position_choices
                self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                  choices=position_choices,
                                                  widget=forms.Select(attrs={'class':'form-control',}),
                                                  )
            except KeyError:
                pass
        # if self.banner.has_show_banner:

            # (none, first, second, third, fourth, fifth) = (0, 1, 2, 3, 4, 5)
            # BANNER_POSITION_CHOICES = (
            #     (none, _("none")),
            #     (first, _("first")),
            #     (second, _("second")),
            #     (third, _("third")),
            #     (fourth, _("fourth")),
            #     (fifth, _("fifth")),
            # )


    def save(self):
        event_banner_image = self.cleaned_data.get('event_banner_image')
        link = self.cleaned_data.get('link')
        user_id = self.cleaned_data.get('user_id')
        banner_type = self.cleaned_data.get('banner_type')
        position = self.clean_position()
        event = self.cleaned_data.get('event')
        event_banner_background_image = self.cleaned_data.get('event_banner_background_image')
        event_banner_background_color = self.cleaned_data.get('event_banner_background_color')


        # log.info(position)
        self.banner.link = link
        # self.banner.position = position
        self.banner.user_id = user_id
        self.banner.banner_type = banner_type

        if event_banner_background_image:
            _background_image = HandleImage(event_banner_background_image)
            self.banner.background_image = _background_image.save()

        self.banner.background_color = event_banner_background_color

        if event_banner_image:
            _image = HandleImage(event_banner_image)
            # file_path = "%s%s.jpg" % (image_path, _image.name)
            # filename = default_storage.save(file_path, ContentFile(_image.image_data))
            self.banner.image = _image.save()

        self.banner.save()

        if event:
            try:
                show = Show_Event_Banner.objects.get(banner = self.banner)
                show.event_id = event
                show.save()
            except Show_Event_Banner.DoesNotExist:
                Show_Event_Banner.objects.create(
                    banner = self.banner,
                    event_id = event,
                )

        if position > 0 and self.banner.position == 0:
            show = Show_Event_Banner.objects.get(banner= self.banner)
            # show.banner = self.banner
            show.position = position
            show.save()
        #
        # elif self.banner.position != position:
        #     show = Show_Event_Banner.objects.get(pk = position)
        #     tmp_show = Show_Event_Banner.objects.get(pk = self.banner.position)
        #     tmp_banner = show.banner
        #     show.banner = self.banner
        #     tmp_show.banner = tmp_banner
        #
        #     show.save()
        #     tmp_show.save()



__author__ = 'edison'
