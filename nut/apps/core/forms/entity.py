from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.log import getLogger

log = getLogger('django')

from apps.core.models import Entity, Sub_Category, Category, Buy_Link
from apps.core.utils.image import HandleImage
from apps.core.utils.fetch import parse_taobao_id_from_url, parse_jd_id_from_url
from apps.core.utils.fetch.taobao import TaoBao
from apps.core.utils.fetch.jd import JD

from django.conf import settings
from urlparse import urlparse
import re

# image_sizes = getattr(settings, 'IMAGE_SIZE', None)
image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
image_host = getattr(settings, 'IMAGE_HOST', None)


def get_sub_category_choices(group_id):
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
    price = forms.DecimalField(
        max_digits=20, decimal_places=2,
        label=_('price'),
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )
    # note = forms.CharField(
    #     label= _('note'),
    #     widget=forms.Textarea(attrs={'class':'form-control'}),
    #     help_text=_(''),
    # )

    def __init__(self, entity, *args, **kwargs):
        super(EntityForm, self).__init__(*args, **kwargs)

        self.entity = entity

        if self.entity.has_top_note:
            self.fields['status'] = forms.ChoiceField(label=_('status'),
                                                  choices=Entity.ENTITY_STATUS_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control'}),
                                                  help_text=_(''))
        else:
            self.fields['status'] = forms.ChoiceField(label=_('status'),
                                                  choices=Entity.NO_SELECTION_ENTITY_STATUS_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control',}),
                                                  help_text=_(''))

        if len(self.entity.images) > 1:
            position_list = list()
            for position in xrange(len(self.entity.images)):
                position_list.append((position, str(position)))
                position_choices = tuple(position_list)
                self.fields['position'] = forms.ChoiceField(label=_('position'),
                            choices=position_choices,
                            widget=forms.Select(attrs={'class':'form-control',}),
                            initial=0,
                            help_text=_(''))
        # log.info(args)
        if len(args):
            group_id = args[0]['category']
        else:

            data = kwargs.get('initial')
            group_id = data['category']


        # log.info("id %s" % group_id)

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

        # id = self.cleaned_data['id']
        brand = self.cleaned_data.get('brand')
        title = self.cleaned_data.get('title')
        price = self.cleaned_data.get('price')
        status = self.cleaned_data.get('status')
        sub_category = self.cleaned_data.get('sub_category')
        position = self.cleaned_data.get('position')

        images = self.entity.images
        a = images[int(position)]
        b = images[0]
        images[int(position)] = b
        images[0] = a

        self.entity.brand = brand
        self.entity.title = title
        self.entity.price = price
        if status:
            self.entity.status = status
        self.entity.category_id = sub_category
        self.entity.images = images
        self.entity.save()

        return self.entity


class EntityImageForm(forms.Form):

    image = forms.ImageField(
        label='Select an Image',
        help_text=_('max. 2 megabytes')
    )

    def __init__(self, entity, *args, **kwargs):
        self.entity = entity
        super(EntityImageForm, self).__init__(*args, **kwargs)

    def save(self):
        image = self.cleaned_data.get('image')

        entity_image = HandleImage(image)
        image_name = image_path + "%s.jpg" % entity_image.name

        if default_storage.exists(image_name):
            image_name = image_host + image_name
        else:
            image_name = image_host + default_storage.save(image_name, ContentFile(entity_image.image_data))
        images = self.entity.images
        images.append(image_name)
        self.entity.images = images
        self.entity.save()


        # for size in image_sizes:
        #     file_path = image_path + "%s.jpg_%sx%s.jpg" % (entity_image.name, size, size)
        #     default_storage.save(file_path, ContentFile(entity_image.resize(size, size)))


        # image_name = image_path + "%s.jpg" % entity_image.name


        # self.entity.save()

class BuyLinkForm(forms.Form):
    # (taobao, jd, ) = xrange(2)
    # ENTITY_STATUS_CHOICES = (
    #     (taobao, _("taobao")),
    #     (jd, _("jd")),
    # )
    #
    #
    # origin_id = forms.IntegerField(
    #     label=_('origin_id'),
    #     widget=forms.TextInput(attrs={'class':'form-control'}),
    #     help_text=_('')
    # )

    # price = forms.FloatField(
    #     label=_('price'),
    #     widget=forms.TextInput(attrs={'class':'form-control'}),
    #     help_text=_('')
    # )
    link = forms.URLField(
        label=_('link'),
        widget=forms.URLInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )

    def __init__(self, entity, *args, **kwargs):
        self.entity_cache = entity
        self.b = None
        super(BuyLinkForm, self).__init__(*args, **kwargs)

        # self.field['source'] = forms.ChoiceField(
        #     label=_('source'),
        #     widget=forms.Select(attrs={'class':'form-control'})
        # )

    def save(self):
        _link = self.cleaned_data.get('link')
        _hostname = urlparse(_link).hostname

        if re.search(r"\b(tmall|taobao|95095)\.(com|hk)$", _hostname) is not None:
            _taobao_id = parse_taobao_id_from_url(_link)
        # log.info(_link)

            try:
                self.b = Buy_Link.objects.get(origin_id=_taobao_id, origin_source="taobao.com",)
                # log.info(buy_link.entity)
                # _data = {
                #     'entity_hash': buy_link.entity.entity_hash,
                # }
            except Buy_Link.DoesNotExist:
                t = TaoBao(_taobao_id)
                # log.info(t.res())
                # res = t.res()
                # log.info(res)
                self.b = Buy_Link(
                    entity = self.entity_cache,
                    origin_id = _taobao_id,
                    cid=t.cid,
                    origin_source = "taobao.com",
                    link = "http://item.taobao.com/item.htm?id=%s" % _taobao_id,
                    price=t.price,
                )
                self.b.save()

        if re.search(r"\b(jd|360buy)\.com$", _hostname) != None:
            _jd_id = parse_jd_id_from_url(_link)
            try:
                self.b = Buy_Link.objects.get(origin_id=_jd_id, origin_source="jd.com",)
            except Buy_Link.DoesNotExist:
                j = JD(_jd_id)
                self.b = Buy_Link(
                    entity = self.entity_cache,
                    origin_id = _jd_id,
                    cid=j.cid,
                    origin_source = "jd.com",
                    link="http://item.jd.com/%s.html" % _jd_id,
                    price=j.price,
                )
                self.b.save()

        return self.b

__author__ = 'edison7500'
