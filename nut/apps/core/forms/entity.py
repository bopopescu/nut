from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

log = getLogger('django')

from apps.core.models import Entity, Sub_Category, Category


def get_sub_category_choices(group_id):
    # log.info(sub_category_list)
    # for row in sub_category_list:
    #     log.info("%s %s" % (row.id, row.title))
    sub_category_list = Sub_Category.objects.filter(group = group_id)
    res = map(lambda x: (x.id, x.title) , sub_category_list)
    return res


def get_category_choices():

    category_list = Category.objects.all()
    res = map(lambda x : (x.id, x.title), category_list)
    return res


class EntityForm(forms.Form):

    (remove, freeze, new, selection) = (-2, -1, 0, 1)
    ENTITY_STATUS_CHOICES = (
        (remove, _("remove")),
        (freeze, _("freeze")),
        (new, _("new")),
        (selection, _("selection")),
)

    id = forms.IntegerField(label=_('entity_id'),
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
        # log.info(args)
        if len(args):
            group_id = args[0]['category']
        else:

            data = kwargs.get('initial')
            group_id = data['category']


        log.info("id %s" % group_id)

        sub_category_choices = get_sub_category_choices(group_id)

        self.fields['category'] = forms.ChoiceField(label=_('category'),
                                                    widget=forms.Select(attrs={'class':'form-control'}),
                                                    choices=get_category_choices(),
                                                    help_text=_('')
                                                    )
        self.fields['sub_category'] = forms.ChoiceField(label=_('sub_category'),
                                                        choices=sub_category_choices,
                                                        widget=forms.Select(attrs={'class':'form-control'}),
                                                        help_text=_(''))
        # log.info(self.fields)

    def clean(self):
        cleaned_data = super(EntityForm, self).clean()
        return cleaned_data

    def save(self):

        id = self.cleaned_data['id']
        brand = self.cleaned_data['brand']
        title = self.cleaned_data['title']
        price = self.cleaned_data['price']
        status = self.cleaned_data['status']
        sub_category = self.cleaned_data.get('sub_category')
        # log.info("id %s", status)
        try:
            entity = Entity.objects.get(pk = id)
        except Entity.DoesNotExist:
            raise

        entity.brand = brand
        entity.title = title
        entity.price = price
        entity.status = status
        entity.category_id = sub_category
        entity.save()

        return entity

__author__ = 'edison7500'
