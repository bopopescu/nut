# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.utils.log import getLogger
from django.utils.translation import gettext_lazy as _

from apps.core.models import Entity, Note, Buy_Link
from apps.core.tasks.entity import fetch_image
from apps.fetch import get_entity_info
from apps.fetch.common import get_url_meta
from apps.report.models import Report


log = getLogger('django')


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


class EntityURLFrom(forms.Form):
    cand_url = forms.URLField(
            label=_('links'),
            widget=forms.URLInput(
                    attrs={'class': 'form-control', 'placeholder': _(
                            'past the product link here')}),

    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(EntityURLFrom, self).__init__(*args, **kwargs)

    def load(self):
        entity_url = self.cleaned_data.get('cand_url')
        data = dict(link_support=False)
        origin_id, origin_source, link = get_url_meta(entity_url)

        buy_link = Buy_Link.objects.filter(origin_id=origin_id,
                                           origin_source=origin_source)
        if buy_link:
            buy_link = buy_link[0]
            data['entity_hash'] = buy_link.entity.entity_hash
        else:
            entity_data = get_entity_info(entity_url, keys=(
                'brand', 'title', 'cid', 'shop_link', 'shop_nick', 'price',
                'foreign_price', 'images', 'chief_image'))
            data.update(
                    user_id=self.request.user.id,
                    user_avatar=self.request.user.profile.avatar_url,
                    cand_url=link,
                    origin_id=origin_id,
                    origin_source=origin_source,
                    **entity_data
            )
        return data


class CreateEntityForm(forms.Form):
    origin_id = forms.CharField(
            widget=forms.TextInput(),
    )

    origin_source = forms.CharField(
            widget=forms.TextInput(),
    )

    cid = forms.IntegerField(
            widget=forms.TextInput(),
    )

    cand_url = forms.URLField(
            widget=forms.URLInput(),
    )

    shop_nick = forms.CharField(
            widget=forms.TextInput()
    )

    shop_link = forms.URLField(
            widget=forms.URLInput()
    )

    title = forms.CharField(
            widget=forms.TextInput()
    )

    brand = forms.CharField(
            widget=forms.TextInput(),
            required=False,
    )

    price = forms.FloatField(
            widget=forms.TextInput(),
    )

    chief_image_url = forms.URLField(
            widget=forms.URLInput(),
    )

    note_text = forms.CharField(
            widget=forms.Textarea(),
    )

    def clean_note_text(self):

        _note_text = self.cleaned_data.get('note_text')
        return _note_text.strip()

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CreateEntityForm, self).__init__(*args, **kwargs)

    def save(self):
        _origin_id = self.cleaned_data.get('origin_id')
        _origin_source = self.cleaned_data.get('origin_source')
        _shop_nick = self.cleaned_data.get('shop_nick')
        _shop_link = self.cleaned_data.get('shop_link')
        _brand = self.cleaned_data.get('brand')
        _title = self.cleaned_data.get('title')
        _cid = self.cleaned_data.get('cid', None)
        _price = self.cleaned_data.get('price')
        _cand_url = self.cleaned_data.get('cand_url')
        _chief_image_url = self.cleaned_data.get('chief_image_url')
        _images = self.data.getlist('thumb_images')
        _note_text = self.cleaned_data.get('note_text')
        _entity_hash = cal_entity_hash(_origin_id + _title + _shop_nick)
        key_string = "%s%s" % (_origin_id, _origin_source)

        key = md5(key_string.encode('utf-8')).hexdigest()

        category_id = cache.get(key)
        if category_id is None:
            category_id = 300

        if _chief_image_url in _images:
            _images.remove(_chief_image_url)

        _images.insert(0, _chief_image_url)

        entity = Entity(
                user_id=self.request.user.id,
                entity_hash=_entity_hash,
                category_id=category_id,
                brand=_brand,
                title=_title,
                price=_price,
                images=_images,
        )
        entity.status = Entity.freeze

        entity.save()
        if not settings.DEBUG:
            fetch_image.delay(entity.images, entity.id)

        Note.objects.create(
                user_id=self.request.user.id,
                entity=entity,
                note=_note_text,
        )

        if 'taobao' in _origin_source:
            Buy_Link.objects.create(
                    entity=entity,
                    origin_id=_origin_id,
                    cid=_cid,
                    origin_source="taobao.com",
                    link="http://item.taobao.com/item.htm?id=%s" % _origin_id,
                    price=_price,
                    default=True,
                    shop_link=_shop_link
            )
        else:
            Buy_Link.objects.create(
                    entity=entity,
                    origin_id=_origin_id,
                    cid=_cid,
                    origin_source=_origin_source,
                    link=_cand_url,
                    price=_price,
                    default=True,
                    shop_link=_shop_link
            )
        return entity


class ReportForms(forms.Form):
    type = forms.ChoiceField(
            label=_("type"),
            choices=Report.TYPE,
            widget=forms.RadioSelect(),
            initial=Report.sold_out,
    )
    content = forms.CharField(
            label=_("additional remarks"),
            widget=forms.Textarea(attrs={'class': 'form-control fs_14 textarea',
                                         'style': "resize: none;",
                                         'rows': '4',}),
            required=False,
    )

    def __init__(self, entity, *args, **kwargs):
        self.entity_cache = entity
        super(ReportForms, self).__init__(*args, **kwargs)

    def save(self, user):
        _content = self.cleaned_data.get('content')
        _type = self.cleaned_data.get('type')
        r = Report(reporter=user, type=_type, comment=_content,
                   content_object=self.entity_cache)
        r.save()
        return r
