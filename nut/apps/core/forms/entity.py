# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

from django import forms
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import ChoiceField
from django.utils.log import getLogger
from django.utils.translation import gettext_lazy as _

from apps.core.forms import get_admin_user_choices
from apps.core.models import Entity, Sub_Category, Category, Buy_Link, Note
from apps.core.tasks.entity import fetch_image
from apps.core.utils.image import HandleImage
from apps.fetch import get_entity_info
from apps.fetch import get_url_meta


log = getLogger('django')
image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
image_host = getattr(settings, 'IMAGE_HOST', None)


def get_sub_category_choices(group_id):
    sub_category_list = Sub_Category.objects.filter(group=group_id).order_by(
            'alias')
    res = map(lambda x: (x.id, x.title), sub_category_list)
    return res


def get_category_choices():
    category_list = Category.objects.filter(status=True)
    res = map(lambda x: (x.id, x.title), category_list)
    return res


def load_entity_info(url):
    origin_id, origin_source = get_url_meta(url, ('origin_id', 'origin_source'))
    entity_data = dict()

    buy_link = Buy_Link.objects.filter(origin_id=origin_id,
                                       origin_source=origin_source)
    if buy_link:
        entity_data['entity_id'] = buy_link[0].entity.id
    else:
        entity_data['origin_id'] = origin_id
        entity_data['origin_source'] = origin_source
        entity_info = get_entity_info(url,
                                      keys=('link', 'brand', 'title', 'cid',
                                            'shop_link', 'shop_nick',
                                            'price', 'thumb_images'))
        entity_data.update(entity_info)
    return entity_data


def cal_entity_hash(hash_string):
    _hash = None
    while True:
        _hash = md5((hash_string + unicode(datetime.now())).encode(
                'utf-8')).hexdigest()[0:8]
        try:
            Entity.objects.get(entity_hash=_hash)
        except Entity.DoesNotExist:
            break
    return _hash


# TODO:
'''
    Entity Form
'''


class EntityForm(forms.Form):
    (remove, freeze, new, selection) = (-2, -1, 0, 1)
    ENTITY_STATUS_CHOICES = (
        (remove, _("remove")),
        (freeze, _("freeze")),
        (new, _("new")),
        (selection, _("selection")),
    )

    creator = forms.CharField(label=_('creator'),
                              widget=forms.TextInput(
                                      attrs={'class': 'form-control',
                                             'readonly': ''}),
                              help_text=_(''))
    brand = forms.CharField(label=_('brand'),
                            widget=forms.TextInput(
                                    attrs={'class': 'form-control'}),
                            required=False,
                            )
    title = forms.CharField(label=_('title'),
                            widget=forms.TextInput(
                                    attrs={'class': 'form-control'}),
                            help_text=_(''))
    price = forms.DecimalField(
            max_digits=20, decimal_places=2,
            label=_('price'),
            widget=forms.NumberInput(attrs={'class': 'form-control'}),
            help_text=_(''),
    )

    def __init__(self, entity, *args, **kwargs):
        super(EntityForm, self).__init__(*args, **kwargs)

        self.entity = entity

        if self.entity.has_top_note:
            self.fields['status'] = forms.ChoiceField(label=_('status'),
                                                      choices=Entity.ENTITY_STATUS_CHOICES,
                                                      widget=forms.Select(
                                                              attrs={
                                                                  'class': 'form-control'}),
                                                      help_text=_(''))
        else:
            self.fields['status'] = forms.ChoiceField(label=_('status'),
                                                      choices=Entity.NO_SELECTION_ENTITY_STATUS_CHOICES,
                                                      widget=forms.Select(
                                                              attrs={
                                                                  'class': 'form-control',}),
                                                      help_text=_(''))

        if len(self.entity.images) > 1:
            position_choices = map(lambda x: (x, x + 1),
                                   range(len(self.entity.images)))
            self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                        choices=position_choices,
                                                        widget=forms.Select(
                                                                attrs={
                                                                    'class': 'form-control',}),
                                                        initial=0,
                                                        help_text=_(''))
        if len(args):
            group_id = args[0]['category']
            sub_category = 0
        else:

            data = kwargs.get('initial')
            group_id = data['category']
            sub_category = data['sub_category']

        sub_category_choices = get_sub_category_choices(group_id)

        self.fields['category'] = forms.ChoiceField(label=_('category'),
                                                    widget=forms.Select(attrs={
                                                        'class': 'form-control',
                                                        'id': 'category',
                                                        'data-init': sub_category}),
                                                    choices=get_category_choices(),

                                                    )
        self.fields['sub_category'] = forms.ChoiceField(label=_('sub_category'),
                                                        choices=sub_category_choices,
                                                        widget=forms.Select(
                                                                attrs={
                                                                    'class': 'form-control',
                                                                    'id': 'sub-category',
                                                                    'data-init': sub_category}),
                                                        help_text=_(''))

    def clean(self):
        cleaned_data = super(EntityForm, self).clean()
        return cleaned_data


class SubCategoryField(ChoiceField):
    def validate(self, value):
        return value


class CreateEntityForm(forms.Form):
    origin_id = forms.CharField(
            label=_('origin id'),
            widget=forms.TextInput(
                    attrs={'class': 'form-control', 'readonly': ''}),
            help_text=_(''),
    )

    origin_source = forms.CharField(
            label=_('origin_source'),
            widget=forms.TextInput(
                    attrs={'class': 'form-control', 'readonly': ''}),
            help_text=_(''),
    )

    title = forms.CharField(
            label=_('title'),
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            help_text=_(''),
    )

    brand = forms.CharField(
            label=_('brand'),
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            required=False,
    )

    price = forms.FloatField(
            label=_('price'),
            widget=forms.NumberInput(attrs={'class': 'form-control'}),
            help_text=_(''),
    )

    cand_url = forms.URLField(
            widget=forms.URLInput(attrs={'class': 'form-control'}),
            show_hidden_initial=True,
            required=False,
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CreateEntityForm, self).__init__(*args, **kwargs)

        self.initial = kwargs.get('initial')
        img_count = len(self.initial['thumb_images'])
        img_choices = map(lambda x: (x, x + 1), xrange(img_count))

        self.fields['main_image'] = forms.ChoiceField(
                label=_('select image'),
                choices=img_choices,
                widget=forms.Select(attrs={'class': 'form-control'}),
                help_text=_(''),
        )
        cate_choices = get_category_choices()
        sub_cate_choices = get_sub_category_choices(cate_choices[0][0]) or []

        self.fields['category'] = forms.ChoiceField(label=_('category'),
                                                    widget=forms.Select(attrs={
                                                        'class': 'form-control',
                                                        'id': 'category'}),
                                                    choices=cate_choices,
                                                    initial=cate_choices[0][0],
                                                    help_text=_(''),
                                                    )
        self.fields['sub_category'] = SubCategoryField(label=_('sub_category'),
                                                       widget=forms.Select(
                                                               attrs={
                                                                   'class': 'form-control',
                                                                   'id': 'sub-category',
                                                               }),
                                                       choices=sub_cate_choices,
                                                       initial=
                                                       sub_cate_choices[0][0],
                                                       help_text=_(''),
                                                       )

        self.fields['content'] = forms.CharField(
                label=_('note'),
                widget=forms.Textarea(attrs={'class': 'form-control'}),
                help_text=_(''),
                required=False,
        )

        self.fields['status'] = forms.ChoiceField(label=_('note status'),
                                                  choices=Note.NOTE_STATUS_CHOICES,
                                                  widget=forms.Select(attrs={
                                                      'class': 'form-control'}),
                                                  initial=Note.normal,
                                                  )

        user_choices = get_admin_user_choices()
        self.fields['user'] = forms.ChoiceField(
                label=_('user'),
                choices=user_choices,
                widget=forms.Select(attrs={'class': 'form-control'}),
                help_text=_(''),
        )

    def save(self):
        _origin_id = self.cleaned_data.get('origin_id')
        _origin_source = self.cleaned_data.get('origin_source')
        _title = self.cleaned_data.get('title')
        _brand = self.cleaned_data.get('brand')
        _price = self.cleaned_data.get('price')
        _sub_category = self.cleaned_data.get('sub_category')
        _main_image = int(self.cleaned_data.get('main_image'))
        _note_text = self.cleaned_data.get('content')
        _status = self.cleaned_data.get('status')
        _user_id = self.cleaned_data.get('user')
        _entity_hash = cal_entity_hash(
                _origin_id + _title + self.initial['shop_nick'])
        log.info("main image %s" % _main_image)

        images = self.initial['thumb_images']
        if _main_image != 0:
            images = self.initial['thumb_images']
            tmp = images.pop(int(_main_image))
            images.insert(0, tmp)
            log.info(images)

        entity = Entity(
                entity_hash=_entity_hash,
                user=self.request.user,
                brand=_brand,
                title=_title,
                price=_price,
                category_id=_sub_category,
                images=images,
        )

        entity.save()
        log.info(entity.images)
        if not settings.DEBUG:
            fetch_image.delay(entity.images, entity.id)

        if _note_text:
            Note.objects.create(
                    user_id=_user_id,
                    entity=entity,
                    note=_note_text,
                    status=_status,
            )

        Buy_Link.objects.create(
                entity=entity,
                origin_id=_origin_id,
                cid=self.initial['cid'],
                origin_source=_origin_source,
                link=self.initial.link,
                price=_price,
                default=True,
        )
        return entity


class EditEntityForm(EntityForm):

    def save(self):
        brand = self.cleaned_data.get('brand')
        title = self.cleaned_data.get('title')
        price = self.cleaned_data.get('price')
        status = self.cleaned_data.get('status')
        sub_category = self.cleaned_data.get('sub_category')
        position = self.cleaned_data.get('position', 0)

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


# TODO:
'''
    Entity Image Form
'''


class EntityImageForm(forms.Form):
    YES_OR_NO = (
        (1, _('yes')),
        (0, _('no')),
    )

    image = forms.ImageField(
            label=_('Select an Image'),
            help_text=_('max. 2 megabytes'),
            required=False,
    )

    image_link = forms.CharField(
            label=_('image link'),
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            required=False,
    )

    is_chief = forms.ChoiceField(
            label=_('chief image'),
            choices=YES_OR_NO,
            widget=forms.Select(attrs={'class': 'form-control'}),
            initial=0,
            help_text=_('set entity cheif Image'),
    )

    def __init__(self, entity, *args, **kwargs):
        self.entity = entity
        super(EntityImageForm, self).__init__(*args, **kwargs)

    def clean_is_chief(self):
        _is_chief = self.cleaned_data.get('is_chief')
        return int(_is_chief)

    def clean_image_link(self):
        _image_link = self.cleaned_data.get('image_link')
        return _image_link.strip()

    def save(self):
        _image = self.cleaned_data.get('image')
        _image_link = self.cleaned_data.get('image_link')
        _is_chief = self.cleaned_data.get('is_chief')

        if _image:
            entity_image = HandleImage(_image)
        else:
            import urllib2
            f = urllib2.urlopen(_image_link)
            entity_image = HandleImage(f)

        image_name = image_path + "%s.jpg" % entity_image.name

        if default_storage.exists(image_name):
            image_name = image_host + image_name
        else:
            image_name = image_host + default_storage.save(
                    image_name,
                    ContentFile(entity_image.image_data))
        images = self.entity.images

        if _is_chief:
            images.insert(0, image_name)
        else:
            images.append(image_name)
        self.entity.images = images
        self.entity.save()


# TODO:
'''
    Entity Buy Link Form
'''


class BuyLinkForm(forms.Form):
    YES_OR_NO = (
        (1, _('yes')),
        (0, _('no')),
    )

    link = forms.URLField(
            label=_('link'),
            widget=forms.URLInput(attrs={'class': 'form-control'}),
            help_text=_(''),
    )

    default = forms.ChoiceField(
            label=_('default'),
            choices=YES_OR_NO,
            widget=forms.Select(attrs={'class': 'form-control'}),
            initial=False,
    )

    def __init__(self, entity, *args, **kwargs):
        self.entity_cache = entity
        self.buy_link = None
        super(BuyLinkForm, self).__init__(*args, **kwargs)

    def save(self):
        link = self.cleaned_data.get('link')
        _default = self.cleaned_data.get('default')
        _default = int(_default)
        origin_id, origin_source = get_url_meta(link,
                                                ('origin_id', 'origin_source'))

        if _default:
            Buy_Link.objects.filter(entity=self.entity_cache).update(
                    default=False)

            buy_link = Buy_Link.objects.filter(origin_id=origin_id,
                                               entity=self.entity_cache,
                                               origin_source=origin_source)
            if buy_link:
                self.buy_link = buy_link[0]
            else:
                entity_data = get_entity_info(link,
                                              keys=('price', 'link', 'cid'))
                self.buy_link = Buy_Link(
                        entity=self.entity_cache,
                        origin_id=origin_id,
                        origin_source=origin_source,
                        default=_default,
                        **entity_data
                )
                self.buy_link.save()
        return self.buy_link


class EditBuyLinkForm(forms.Form):
    YES_OR_NO = (
        (1, _('yes')),
        (0, _('no')),
    )

    link = forms.URLField(
            label=_('link'),
            widget=forms.URLInput(attrs={'class': 'form-control'}),
            help_text=_(''),
    )

    default = forms.ChoiceField(
            label=_('default'),
            choices=YES_OR_NO,
            widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, buy_link, *args, **kwargs):
        self.buy_link = buy_link
        super(EditBuyLinkForm, self).__init__(*args, **kwargs)

    def save(self):
        _link = self.cleaned_data.get('link')
        _default = self.cleaned_data.get('default')
        _default = int(_default)

        if _default:
            Buy_Link.objects.filter(entity=self.buy_link.entity).update(
                    default=False)

        self.buy_link.default = _default
        self.buy_link.link = _link
        self.buy_link.save()
        return self.buy_link


__author__ = 'edison7500'
