# -*- coding: utf-8 -*-

import re
from datetime import datetime
from hashlib import md5
from urlparse import urlparse

from apps.core.fetch import parse_taobao_id_from_url, \
    parse_jd_id_from_url, parse_kaola_id_from_url
from apps.core.fetch.amazon import Amazon
from apps.core.fetch.booking import Booking
from apps.core.fetch.kaola import Kaola
from apps.core.fetch.six_pm import SixPM
from apps.core.fetch.taobao import TaoBao
from django import forms
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import ChoiceField
from django.utils.log import getLogger
from django.utils.translation import gettext_lazy as _

from apps.core.fetch.jd import JD
from apps.core.forms import get_admin_user_choices
from apps.core.models import Entity, Sub_Category, Category, Buy_Link, Note
from apps.core.tasks.entity import fetch_image
from apps.core.utils.image import HandleImage



log = getLogger('django')
# image_sizes = getattr(settings, 'IMAGE_SIZE', None)
image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
image_host = getattr(settings, 'IMAGE_HOST', None)


def get_sub_category_choices(group_id):
    sub_category_list = Sub_Category.objects.filter(group=group_id).order_by(
        'alias')
    res = map(lambda x: (x.id, x.title), sub_category_list)
    return res


def get_category_choices():
    category_list = Category.objects.filter(status=True)
    # log.info(category_list)
    res = map(lambda x: (x.id, x.title), category_list)
    return res


def load_entity_info(url):
    _link = url
    _hostname = urlparse(_link).hostname

    # log.info(_hostname)
    _data = dict()

    if re.search(r"\b(jd|360buy)\.com$", _hostname) != None:
        _jd_id = parse_jd_id_from_url(_link)
        # log.info(_jd_id)
        try:
            buy_link = Buy_Link.objects.get(origin_id=_jd_id,
                                            origin_source="jd.com", )
            _data = {
                'entity_id': buy_link.entity.id,
            }
        except Buy_Link.DoesNotExist:
            j = JD(_jd_id)

            # print "OKOKOKOKOKO"
            log.info("category id %s" % j.cid)
            _data = {
                # 'user_id': self.request.user.id,
                # 'user_avatar': self.request.user.profile.avatar_url,
                'cand_url': _link,
                'origin_id': _jd_id,
                'origin_source': 'jd.com',
                'brand': j.brand,
                'title': j.title,
                'cid': j.cid,
                # 'taobao_title': res['desc'],
                'shop_link': j.shop_link,
                'shop_nick': j.nick,
                'price': j.price,
                # 'chief_image_url' : j.imgs[0],
                'thumb_images': j.imgs,
                # 'selected_category_id':
            }
            # print _data
            # pass
            # return jd_info(self.request, _link)

    if re.search(r"\b(tmall|taobao|95095)\.(com|hk)$", _hostname) is not None:
        _taobao_id = parse_taobao_id_from_url(_link)
        log.info("taobao id %s" % _taobao_id)

        try:
            buy_link = Buy_Link.objects.get(origin_id=_taobao_id,
                                            origin_source="taobao.com", )
            # log.info(buy_link.entity)
            _data = {
                'entity_id': buy_link.entity.id,
            }
        except Buy_Link.DoesNotExist:
            # log.info("OKOKOKO")
            t = TaoBao(_link)
            # log.info(t.res())
            # res = t.res()
            _data = {
                # 'user_id': self.request.user.id,
                # 'user_avatar': self.request.user.profile.avatar_url,
                'cand_url': _link,
                'origin_id': _taobao_id,
                'origin_source': 'taobao.com',
                'cid': t.cid,
                'title': t.desc,
                'shop_nick': t.nick,
                'shop_link': t.shoplink,
                'price': t.price,
                # 'chief_image_url' : t.images[0],
                'thumb_images': t.images,
                # 'selected_category_id':
            }
            log.info(t.images)
        except Buy_Link.MultipleObjectsReturned:
            buy_link = Buy_Link.objects.filter(origin_id=_taobao_id,
                                               origin_source="taobao.com").first()
            _data = {
                'entity_id': buy_link.entity.id,
            }

    if re.search(r"\b(kaola)\.com$", _hostname) != None:
        # log.info(_hostname)
        # _kaola_id = parse_kaola_id_from_url(_link)
        # log.info(_link)
        k = Kaola(_link)
        try:
            buy_link = Buy_Link.objects.get(origin_id=k.origin_id,
                                            origin_source=k.hostname)
            # log.info(buy_link.entity)
            _data = {
                'entity_id': buy_link.entity.id,
            }
        except Buy_Link.DoesNotExist:
            _data = {
                'cand_url': k.url,
                'origin_id': k.origin_id,
                'origin_source': k.hostname,
                'brand': k.brand,
                'title': k.desc,
                'thumb_images': k.images,
                'price': k.price,
                'cid': k.cid,
                'shop_link': k.shop_link,
                'shop_nick': k.nick,
            }

            log.info(_data)
    if re.search(r"\b(booking)\.com$", _hostname) != None:
        # _booking_id = parse_booking_id_from_url(_link)
        b = Booking(_link)
        try:
            buy_link = Buy_Link.objects.get(origin_id=b.origin_id,
                                            origin_source=b.hostname, )
            # log.info(buy_link.entity)
            _data = {
                'entity_id': buy_link.entity.id,
            }
        except Buy_Link.DoesNotExist:
            # b = Booking(_link)
            # k.fetch_html()
            # log.info(k.desc)
            _data = {
                'cand_url': b.url,
                'origin_id': b.origin_id,
                'origin_source': b.hostname,
                'brand': b.brand,
                'title': b.desc,
                'thumb_images': b.images,
                'price': b.price,
                'cid': b.cid,
                'shop_link': b.shop_link,
                'shop_nick': b.nick,
            }

    if re.search(r"\b(amazon)\.(cn|com|co\.jp)$", _hostname) != None:
        a = Amazon(_link)
        try:
            buy_link = Buy_Link.objects.get(origin_id=a.origin_id,
                                            origin_source=a.hostname)
            _data = {
                'entity_id': buy_link.entity.id,
            }
        except Buy_Link.DoesNotExist, e:
            _data = {
                'cand_url': a.url,
                'origin_id': a.origin_id,
                'origin_source': a.hostname,
                'title': a.desc,
                'thumb_images': a.images,
                'price': a.price,
                'cid': a.cid,
                'brand': a.brand,
                'shop_link': a.shop_link,
                'shop_nick': a.nick,
            }

    if re.search(r"6pm\.com", _hostname) != None:
        pm = SixPM(_link)
        try:
            buy_link = Buy_Link.objects.get(origin_id=pm.origin_id,
                                            origin_source=pm.hostname)
            _data = {
                'entity_id': buy_link.entity.id,
            }
        except Buy_Link.DoesNotExist, e:
            _data = {
                'cand_url': pm.url,
                'origin_id': pm.origin_id,
                'origin_source': pm.hostname,
                'title': pm.desc,
                'thumb_images': pm.images,
                'price': pm.price,
                'cid': pm.cid,
                'brand': pm.brand,
                'shop_link': pm.shop_link,
                'shop_nick': pm.nick,
            }
    return _data

    # return


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

    # id = forms.IntegerField(label=_('entity_id'),
    #                      widget=forms.NumberInput(attrs={'class':'form-control', 'readonly':''}),
    # help_text=_(''))
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
    # intro = forms.CharField(label=_('intro'), widget=forms.Textarea(attrs={'class':'form-control'}),
    #                         required=False,
    #                         )
    price = forms.DecimalField(
        max_digits=20, decimal_places=2,
        label=_('price'),
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text=_(''),
    )
    # note = forms.CharField(
    #     label= _('note'),
    #     widget=forms.Textarea(attrs={'class':'form-control'}),
    #
    # )

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
                                                              'class': 'form-control', }),
                                                      help_text=_(''))

        if len(self.entity.images) > 1:
            # position_list = list()
            # for position in xrange(len(self.entity.images)):
            #     position_list.append((position, str(position)))
            #     position_choices = tuple(position_list)
            position_choices = map(lambda x: (x, x + 1),
                                   range(len(self.entity.images)))
            self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                        choices=position_choices,
                                                        widget=forms.Select(
                                                            attrs={
                                                                'class': 'form-control', }),
                                                        initial=0,
                                                        help_text=_(''))
        # log.info(args)
        if len(args):
            group_id = args[0]['category']
            sub_category = 0
        else:

            data = kwargs.get('initial')
            group_id = data['category']
            sub_category = data['sub_category']

        # log.info("id %s" % group_id)

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
        # log.info(self.fields)

    def clean(self):
        cleaned_data = super(EntityForm, self).clean()
        return cleaned_data


class SubCategoryField(ChoiceField):
    def validate(self, value):
        return value


class CreateEntityForm(forms.Form):
    origin_id = forms.CharField(
        label=_('origin id'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
        help_text=_(''),
    )

    origin_source = forms.CharField(
        label=_('origin_source'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
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

    # content = forms.CharField(
    #     label=_('note'),
    #     widget=forms.Textarea(attrs={'class': 'form-control'}),
    #
    # )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CreateEntityForm, self).__init__(*args, **kwargs)

        # if len(args):
        #     group_id = args[0]['category']
        #     img_count = len(args[0]['thumb_images'])
        #     # images = args[0]['thumb_images']
        # else:

        self.initial = kwargs.get('initial')
        img_count = len(self.initial['thumb_images'])

        # log.info("id %s" % group_id)

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
                                                       initial=sub_cate_choices[0][0],
                                                        help_text=_(''),
                                                        )
        # def sub_validate(self, value):
        #     return value
        # self.fields['sub_category'].validate = sub_validate


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

    # def clean_status(self):
    #     _status = self.cleaned_data.get('status')
    #     return int(_status)

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
        # log.info(self.initial['shop_nick'])
        _entity_hash = cal_entity_hash(
            _origin_id + _title + self.initial['shop_nick'])
        log.info("main image %s" % _main_image)

        images = self.initial['thumb_images']
        if _main_image != 0:
            images = self.initial['thumb_images']
            tmp = images.pop(int(_main_image))
            images.insert(0, tmp)
            log.info(images)
        # log.info("image %s", tmp)
        # log.info(images)

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

        if "taobao" in _origin_source:
            Buy_Link.objects.create(
                entity=entity,
                origin_id=_origin_id,
                cid=self.initial['cid'],
                origin_source=_origin_source,
                link="http://item.taobao.com/item.htm?id=%s" % _origin_id,
                price=_price,
                default=True,
            )
        elif "jd.com" in _origin_source:
            Buy_Link.objects.create(
                entity=entity,
                origin_id=_origin_id,
                cid=self.initial['cid'],
                origin_source=_origin_source,
                link="http://item.jd.com/%s.html" % _origin_id,
                price=_price,
                default=True,
            )
        # elif "booking.com" in _origin_source:
        #     _link = self.cleaned_data.get('cand_url')
        #     Buy_Link.objects.create(
        #         entity = entity,
        #         origin_id = _origin_id,
        #         cid = self.initial['cid'],
        #         origin_source = _origin_source,
        #         link = _link,
        #         price = _price,
        #         default = True,
        #     )
        else:
            _link = self.cleaned_data.get('cand_url')
            Buy_Link.objects.create(
                entity=entity,
                origin_id=_origin_id,
                cid=self.initial['cid'],
                origin_source=_origin_source,
                link=_link,
                price=_price,
                default=True,
            )
        return entity


class EditEntityForm(EntityForm):
    # def clean_status(self):
    #     status = self.cleaned_data.get('status')
    #     return int(status)

    def save(self):
        # id = self.cleaned_data['id']
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
            # fetch_image.delay(entity.images, entity.id)

        image_name = image_path + "%s.jpg" % entity_image.name

        if default_storage.exists(image_name):
            image_name = image_host + image_name
        else:
            image_name = image_host + default_storage.save(image_name,
                                                           ContentFile(
                                                               entity_image.image_data))
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
    #
    # origin_id = forms.IntegerField(
    #     label=_('origin_id'),
    #     widget=forms.TextInput(attrs={'class':'form-control'}),
    #
    # )

    # price = forms.FloatField(
    #     label=_('price'),
    #     widget=forms.TextInput(attrs={'class':'form-control'}),
    #
    # )
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
        self.b = None
        super(BuyLinkForm, self).__init__(*args, **kwargs)

        # self.field['source'] = forms.ChoiceField(
        #     label=_('source'),
        #     widget=forms.Select(attrs={'class':'form-control'})
        # )

    def save(self):
        _link = self.cleaned_data.get('link')
        _default = self.cleaned_data.get('default')
        _default = int(_default)

        _hostname = urlparse(_link).hostname

        if _default:
            Buy_Link.objects.filter(entity=self.entity_cache).update(
                default=False)

        if re.search(r"\b(tmall|taobao|95095)\.(com|hk)$",
                     _hostname) is not None:
            _taobao_id = parse_taobao_id_from_url(_link)

            try:
                self.b = Buy_Link.objects.get(origin_id=_taobao_id,
                                              entity=self.entity_cache,
                                              origin_source="taobao.com", )
                # log.info(buy_link.entity)
                # _data = {
                #     'entity_hash': buy_link.entity.entity_hash,
                # }
            except Buy_Link.DoesNotExist:
                t = TaoBao(_link)
                # log.info(t.res())
                # res = t.res()
                # log.info(res)
                self.b = Buy_Link(
                    entity=self.entity_cache,
                    origin_id=_taobao_id,
                    cid=t.cid,
                    origin_source="taobao.com",
                    link="http://item.taobao.com/item.htm?id=%s" % _taobao_id,
                    price=t.price,
                    default=_default,
                )
                self.b.save()

        if re.search(r"\b(jd|360buy)\.com$", _hostname) != None:
            _jd_id = parse_jd_id_from_url(_link)
            try:
                self.b = Buy_Link.objects.get(origin_id=_jd_id,
                                              entity=self.entity_cache,
                                              origin_source="jd.com", )
            except Buy_Link.DoesNotExist:
                j = JD(_jd_id)
                self.b = Buy_Link(
                    entity=self.entity_cache,
                    origin_id=_jd_id,
                    cid=j.cid,
                    origin_source="jd.com",
                    link="http://item.jd.com/%s.html" % _jd_id,
                    price=j.price,
                    default=_default,
                )
                self.b.save()

        if re.search(r"\b(kaola)\.com$", _hostname) != None:
            _kaola_id = parse_kaola_id_from_url(_link)
            try:
                self.b = Buy_Link.objects.get(origin_id=_kaola_id,
                                              entity=self.entity_cache,
                                              origin_source="kaola.com", )
            except Buy_Link.DoesNotExist:
                k = Kaola(_kaola_id)
                self.b = Buy_Link(
                    entity=self.entity_cache,
                    origin_id=_kaola_id,
                    cid=k.cid,
                    origin_source="kaola.com",
                    link="http://www.kaola.com/product/%s.html" % _kaola_id,
                    price=k.price,
                    default=_default,
                )
                self.b.save()

        if re.search(r"\b(booking)\.com$", _hostname) != None:
            # _booking_id = parse_booking_id_from_url(_link)
            b = Booking(_link)
            try:
                self.b = Buy_Link.objects.get(origin_id=b.origin_id,
                                              entity=self.entity_cache,
                                              origin_source=b.hostname, )
            except Buy_Link.DoesNotExist:
                b = Booking(_link)
                self.b = Buy_Link(
                    entity=self.entity_cache,
                    origin_id=b.origin_id,
                    cid=b.cid,
                    origin_source=b.hostname,
                    link=b.url,
                    price=b.price,
                    default=_default,
                )
                self.b.save()

        if re.search(r"\b(amazon)\.(cn|com)$", _hostname) != None:
            a = Amazon(_link)
            try:
                self.b = Buy_Link.objects.get(origin_id=a.origin_id,
                                              origin_source=a.hostname)

            except Buy_Link.DoesNotExist, e:
                self.b = Buy_Link(
                    entity=self.entity_cache,
                    origin_id=a.origin_id,
                    cid=a.cid,
                    origin_source=a.hostname,
                    link=a.url,
                    price=a.price,
                    default=_default,
                )
                self.b.save()
                # print self.b.link
        return self.b


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
        # initial=0,

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
