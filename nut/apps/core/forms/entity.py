from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

log = getLogger('django')

from apps.core.models import Entity


class EntityForm(forms.Form):

    (remove, freeze, new, selection) = (-2, -1, 0, 1)
    ENTITY_STATUS_CHOICES = (
        (remove, _("remove")),
        (freeze, _("freeze")),
        (new, _("new")),
        (selection, _("selection")),
)

    id = forms.CharField(label=_('entity_id'),
                         widget=forms.NumberInput(attrs={'class':'form-control', 'readonly':''}),
                         help_text=_(''))
    creator = forms.CharField(label=_('creator'),
                              widget=forms.TextInput(attrs={'class':'form-control', 'readonly':''}),
                              help_text=_(''))
    brand = forms.CharField(label=_('brand'),
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            required=False,
                            help_text=_(''))
    title = forms.CharField(label=_('title'),
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            help_text=_(''))
    # intro = forms.CharField(label=_('intro'), widget=forms.Textarea(attrs={'class':'form-control'}),
    #                         required=False,
    #                         help_text=_(''))
    price = forms.DecimalField(max_digits=20, decimal_places=2,
                               label=_('price'),
                               widget=forms.NumberInput(attrs={'class':'form-control'}),
                               help_text=_(''))

    def __init__(self, *args, **kwargs):
        super(EntityForm, self).__init__(*args, **kwargs)
        self.fields['status'] = forms.ChoiceField(label=_('status'),
                                                  choices=Entity.ENTITY_STATUS_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control'}),
                                                  help_text=_(''))
        self.fields['sub_category'] = forms.ChoiceField(label=_('sub_category'),
                                                        widget=forms.Select(attrs={'class':'form-control'}),
                                                        help_text=_(''))

    def clean(self):
        cleaned_data = super(EntityForm, self).clean()
        return cleaned_data

    def save(self):

        id = self.cleaned_data['id']
        brand = self.cleaned_data['brand']
        title = self.cleaned_data['title']
        price = self.cleaned_data['price']
        status = self.cleaned_data['status']
        # log.info("id %s", id)
        try:
            entity = Entity.objects.get(pk = id)
        except Entity.DoesNotExist:
            raise

        entity.brand = brand
        entity.title = title
        entity.price = price
        entity.status = status
        entity.save()

__author__ = 'edison7500'
