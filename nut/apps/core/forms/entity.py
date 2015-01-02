from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.log import getLogger

log = getLogger('django')

from apps.core.models import Entity, Sub_Category, Category, Buy_Link, Note
from apps.core.utils.image import HandleImage
from apps.core.utils.fetch import parse_taobao_id_from_url, parse_jd_id_from_url
from apps.core.utils.fetch.taobao import TaoBao
from apps.core.utils.fetch.jd import JD
from apps.core.tasks.entity import fetch_image

from django.conf import settings
from urlparse import urlparse
import re
from hashlib import md5
from datetime import datetime


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
    YES_OR_NO = (
        (True, _('yes')),
        (False, _('no')),
    )
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

    default = forms.ChoiceField(
        label=_('default'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
        initial=False,
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
        _default = self.cleaned_data.get('default')
        _default = bool(_default)
        # log.info(type(bool(_default)))
        _hostname = urlparse(_link).hostname

        if _default:
            Buy_Link.objects.filter(entity=self.entity_cache).update(default=False)

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
                    default=_default,
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
                    default=_default,
                )
                self.b.save()

        return self.b


class EntityURLFrom(forms.Form):
    cand_url = forms.URLField(
        label=_('links'),
        widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':_('copy item link')}),
        help_text = _(''),
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(EntityURLFrom, self).__init__(*args, **kwargs)

    def load(self):
        _link = self.cleaned_data.get('cand_url')
        _hostname = urlparse(_link).hostname

        log.info(_hostname)
        _data = dict()

        if re.search(r"\b(jd|360buy)\.com$", _hostname) != None:
            _jd_id = parse_jd_id_from_url(_link)
            # log.info(_jd_id)
            try:
                buy_link = Buy_Link.objects.get(origin_id=_jd_id, origin_source="jd.com",)
                _data = {
                    'entity_hash': buy_link.entity.entity_hash,
                }
            except Buy_Link.DoesNotExist:
                j = JD(_jd_id)

                # print "OKOKOKOKOKO"
                log.info(j.brand)
                _data = {
                    'user_id': self.request.user.id,
                    'user_avatar': self.request.user.profile.avatar_url,
                    'cand_url': _link,
                    'jd_id': _jd_id,
                    'brand': j.brand,
                    'jd_title': j.title,
                    'cid': j.cid,
                    # 'taobao_title': res['desc'],
                    # 'shop_nick': res['nick'],
                    'shop_link': j.shop_link,
                    'price': j.price,
                    'chief_image_url' : j.imgs[0],
                    'thumb_images': j.imgs,
                    # 'selected_category_id':
                }
                # print _data
            # pass
            # return jd_info(self.request, _link)

        if re.search(r"\b(tmall|taobao|95095)\.(com|hk)$", _hostname) is not None:
            _taobao_id = parse_taobao_id_from_url(_link)
            # log.info(_taobao_id)

            try:
                buy_link = Buy_Link.objects.get(origin_id=_taobao_id, origin_source="taobao.com",)
                log.info(buy_link.entity)
                _data = {
                    'entity_hash': buy_link.entity.entity_hash,
                }
            except Buy_Link.DoesNotExist:
                # log.info("OKOKOKO")
                t = TaoBao(_taobao_id)
                # log.info(t.res())
                res = t.res()
                _data = {
                    'user_id': self.request.user.id,
                    'user_avatar': self.request.user.profile.avatar_url,
                    'cand_url': _link,
                    'taobao_id': _taobao_id,
                    'cid': res['cid'],
                    'taobao_title': res['desc'],
                    'shop_nick': res['nick'],
                    'shop_link': res['shop_link'],
                    'price': res['price'],
                    'chief_image_url' : res['imgs'][0],
                    'thumb_images': res["imgs"],
                    # 'selected_category_id':
                }

        return _data



class CreateEntityForm(forms.Form):

    taobao_id = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )
    jd_id = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )
    cid = forms.IntegerField(
        widget=forms.TextInput(),
    )
    # cand_url = forms.URLField(
    #     widget=forms.URLInput(),
    # )
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

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CreateEntityForm, self).__init__(*args, **kwargs)

    def save(self):
        _taobao_id = self.cleaned_data.get('taobao_id')
        _jd_id = self.cleaned_data.get('jd_id')
        _shop_nick = self.cleaned_data.get('shop_nick')
        _brand = self.cleaned_data.get('brand')
        _title = self.cleaned_data.get('title')
        _cid = self.cleaned_data.get('cid', None)
        _price = self.cleaned_data.get('price')
        _chief_image_url = self.cleaned_data.get('chief_image_url')
        _images = self.data.getlist('thumb_images')

        _note_text = self.cleaned_data.get('note_text')
        # _cand_url = self.cleaned_data.get('cand_url')

        log.info("category %s" % _cid)
        _entity_hash = cal_entity_hash(_taobao_id+_title+_shop_nick)

        category_id = 300
        # try:
        #     cate = Taobao_Item_Category_Mapping.objects.get(taobao_category_id = _cid)
        #     category_id = cate.neo_category_id
        # except Taobao_Item_Category_Mapping.DoesNotExist:
        #     pass

        if _chief_image_url in _images:
            _images.remove(_chief_image_url)

        _images.insert(0, _chief_image_url)

        log.info("category %s" % _cid)

        entity = Entity(
            user_id=self.request.user.id,
            entity_hash= _entity_hash,
            category_id = category_id,
            brand=_brand,
            title=_title,
            price=_price,
            images=_images,
        )

        log.info(entity.images)

        entity.save()
        # log.info(entity.images)
        fetch_image.delay(entity.images, entity.id)

        Note.objects.create(
            user_id = self.request.user.id,
            entity = entity,
            note = _note_text,
        )

        # _hostname = urlparse(_cand_url).hostname
        if _taobao_id:
            Buy_Link.objects.create(
                entity = entity,
                origin_id = _taobao_id,
                cid = _cid,
                origin_source = "taobao.com",
                link = "http://item.taobao.com/item.htm?id=%s" % _taobao_id,
                price = _price,
            )
        else:
            Buy_Link.objects.create(
                entity = entity,
                origin_id = _jd_id,
                cid = _cid,
                origin_source = "jd.com",
                link = "http://item.jd.com/%s.html" % _jd_id,
                price = _price,
            )


        return entity



def load_entity_info(url):
    _link = url
    _hostname = urlparse(_link).hostname

        # log.info(_hostname)
    _data = dict()

    if re.search(r"\b(jd|360buy)\.com$", _hostname) != None:
            _jd_id = parse_jd_id_from_url(_link)
            # log.info(_jd_id)
            try:
                buy_link = Buy_Link.objects.get(origin_id=_jd_id, origin_source="jd.com",)
                _data = {
                    'entity_hash': buy_link.entity.entity_hash,
                }
            except Buy_Link.DoesNotExist:
                j = JD(_jd_id)

                # print "OKOKOKOKOKO"
                log.info(j.brand)
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
                    # 'shop_nick': res['nick'],
                    'shop_link': j.shop_link,
                    'price': j.price,
                    'chief_image_url' : j.imgs[0],
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
                buy_link = Buy_Link.objects.get(origin_id=_taobao_id, origin_source="taobao.com",)
                log.info(buy_link.entity)
                _data = {
                    'entity_hash': buy_link.entity.entity_hash,
                }
            except Buy_Link.DoesNotExist:
                log.info("OKOKOKO")
                t = TaoBao(_taobao_id)
                # log.info(t.res())
                res = t.res()
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
                    'chief_image_url' : t.images[0],
                    'thumb_images': t.images,
                    # 'selected_category_id':
                }

    return _data

    # return

def cal_entity_hash(hash_string):
    _hash = None
    while True:
        _hash = md5((hash_string + unicode(datetime.now())).encode('utf-8')).hexdigest()[0:8]
        try:
            Entity.objects.get(entity_hash = _hash)
        except Entity.DoesNotExist:
            break
    return _hash



__author__ = 'edison7500'
