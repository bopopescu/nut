from django import forms
from django.utils.translation import gettext_lazy as _
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
from django.utils.log import getLogger
from apps.core.utils.image import HandleImage
# from base.handle_image import HandleImage
from apps.core.models import Show_Editor_Recommendation, Editor_Recommendation, Event

log = getLogger('django')

# from django.conf import settings
# image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')

class BaseRecommendationForm(forms.Form):

    link = forms.URLField(
        label=_('link'),
        widget=forms.TextInput(attrs={'class':'form-control'}),

    )
    editor_recommend_image = forms.FileField(
        label=_('event banner image'),
        widget=forms.FileInput(attrs={'class':'controls'}),

        required=False,
    )

    section =  forms.ChoiceField(
        choices=Show_Editor_Recommendation.RECOMMENDATION_SECTION_CHOICE,
        required=False,
    )


    def __init__(self, *args, **kwargs):
        super(BaseRecommendationForm, self).__init__(*args, **kwargs)
        # (none, first, second, third, fourth) = (0, 1, 2, 3, 4)
        # BANNER_POSITION_CHOICES = (
        #     (none, _("none")),
        #     (first, _("first")),
        #     (second, _("second")),
        #     (third, _("third")),
        #     (fourth, _("fourth")),
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


    def clean_position(self):
        _position = self.cleaned_data.get('position', 0)
        return int(_position)


class CreateEditorRecommendForms(BaseRecommendationForm):

    def save(self):
        link = self.cleaned_data.get('link')
        editor_recommend_image = self.cleaned_data.get('editor_recommend_image')
        event = self.cleaned_data.get('event')
        section = self.cleaned_data.get('section')
        # position = self.clean_position()
        # log.info(event_banner_image)
        _image = HandleImage(editor_recommend_image)
        filename = _image.save()
        # file_path = "%s%s.jpg" % (image_path, _image.name)
        # default_storage.save(file_path, ContentFile(_image.image_data))
        # log.info(f)
        #
        _recommendation = Editor_Recommendation.objects.create(
            link = link,
            image = filename,
        )


        #
        # if position > 0:
        #     show_list = Show_Editor_Recommendation.objects.filter(event_id = event, position = position)
        #
        #     show_list.update(position = 0)
        #     try:
        #         show = Show_Editor_Recommendation.objects.get(position = position)
        #         show.recommendation = _recommendation
        #         show.save()
        #     except Show_Editor_Recommendation.DoesNotExist:
        #         Show_Editor_Recommendation.objects.create(
        #             recommendation =_recommendation
        #         )

        if event:
            try:
                show = Show_Editor_Recommendation.objects.get(recommendation = _recommendation)
                show.event_id = event
                show.save()
            except Show_Editor_Recommendation.DoesNotExist, e:
                Show_Editor_Recommendation.objects.create(
                    recommendation = _recommendation,
                    event_id = event,
                    section = section
                )

        return _recommendation


class EditEditorRecommendForms(BaseRecommendationForm):

    def __init__(self, recommendation, *args, **kwargs):
        self.recommendation = recommendation
        super(EditEditorRecommendForms, self).__init__(*args, **kwargs)
        # if self.recommendation.has_show_banner:
        #     (none, first, second, third, fourth) = (0, 1, 2, 3, 4)
        #     BANNER_POSITION_CHOICES = (
        #         # (none, _("none")),
        #         (first, _("first")),
        #         (second, _("second")),
        #         (third, _("third")),
        #         (fourth, _("fourth")),
        #     )
        #     self.fields['position'] = forms.ChoiceField(label=_('position'),
        #                                           choices=BANNER_POSITION_CHOICES,
        #                                           widget=forms.Select(attrs={'class':'form-control',}),
        #                                           )
        if self.recommendation.event:
            try:
                # event_id = kwargs['data']['event']
                positions = Show_Editor_Recommendation.objects.filter(event = self.recommendation.event).count()
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


    def save(self):
        link = self.cleaned_data.get('link')
        editor_recommend_image = self.cleaned_data.get('editor_recommend_image')
        link = self.cleaned_data.get('link')
        position = self.clean_position()
        event = self.cleaned_data.get('event')


        # log.info(position)

        if editor_recommend_image:
            _image = HandleImage(editor_recommend_image)
            # file_path = "%s%s.jpg" % (image_path, _image.name)
            # filename = default_storage.save(file_path, ContentFile(_image.image_data))
            self.recommendation.image = _image.save()


        self.recommendation.link = link
        self.recommendation.save()

        if event:
            try:
                show = Show_Editor_Recommendation.objects.get(recommendation = self.recommendation)
                show.event_id = event
                show.save()
            except Show_Editor_Recommendation.DoesNotExist, e:
                Show_Editor_Recommendation.objects.create(
                    recommendation = self.recommendation,
                    event_id = event,
                )

        if position > 0:
            # try:
            # log.info(position)
            show_list = Show_Editor_Recommendation.objects.filter(event_id = event, position = position)

            show_list.update(position = 0)
            # show.save()
            # except Show_Editor_Recommendation.DoesNotExist:
            #     pass


            show = Show_Editor_Recommendation.objects.get(recommendation= self.recommendation)
            # show.banner = self.banner
            show.position = position
            show.save()
        else:
            show = Show_Editor_Recommendation.objects.get(recommendation= self.recommendation)
            show.position = position
            show.save()
        # if position > 0 and self.recommendation.position == 0:
        #     try:
        #         show = Show_Editor_Recommendation.objects.get(pk= position)
        #         show.recommendation = self.recommendation
        #         show.save()
        #     except Show_Editor_Recommendation.DoesNotExist:
        #         Show_Editor_Recommendation.objects.create(
        #             recommendation = self.recommendation,
        #         )
        # elif self.recommendation.position != position:
        #     show = Show_Editor_Recommendation.objects.get(pk = position)
        #     tmp_show = Show_Editor_Recommendation.objects.get(pk = self.recommendation.position)
        #     recommendation = show.recommendation
        #     show.recommendation = self.recommendation
        #     tmp_show.recommendation = recommendation
        #
        #     show.save()
        #     tmp_show.save()



__author__ = 'edison'
