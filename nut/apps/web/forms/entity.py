# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger
from django.core.cache import cache

from apps.core.models import Entity, Note, Buy_Link
from apps.core.utils.fetch.taobao import TaoBao
from apps.core.utils.fetch.jd import JD
from apps.core.utils.fetch import parse_jd_id_from_url, parse_taobao_id_from_url
from apps.core.tasks.entity import fetch_image

from apps.report.models import Report

from urlparse import urlparse
import re
from datetime import datetime
from hashlib import md5


log = getLogger('django')


# from apps.core.models import Buy_Link


# def parse_taobao_id_from_url(url):
#     params = url.split("?")[1]
#     for param in params.split("&"):
#         tokens = param.split("=")
#         if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
#             return tokens[1]
#     return None
#
# def parse_jd_id_from_url(url):
#     ids = re.findall(r'\d+',url)
#     if len(ids) > 0:
#         return ids[0]
#     else:
#         return None

def cal_entity_hash(hash_string):
    _hash = None
    while True:
        _hash = md5((hash_string + unicode(datetime.now())).encode('utf-8')).hexdigest()[0:8]
        try:
            Entity.objects.get(entity_hash = _hash)
        except Entity.DoesNotExist:
            break
    return _hash



class EntityURLFrom(forms.Form):
    cand_url = forms.URLField(
        label=_('links'),
        widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':_('复制商品链接')}),
        help_text = _(''),
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(EntityURLFrom, self).__init__(*args, **kwargs)

    def load(self):
        _link = self.cleaned_data.get('cand_url')
        _hostname = urlparse(_link).hostname

        log.info(_hostname)
        _data = {'link_support':False}

        if re.search(r"\b(jd|360buy)\.com$", _hostname) != None:
            _data['link_support'] = True;
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
                _data.update({
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
                });

                return _data;
                # print _data
            # pass
            # return jd_info(self.request, _link)

        if re.search(r"\b(tmall|taobao|95095)\.(com|hk)$", _hostname) is not None:
            _data['link_support'] = True;
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
                _data.update({
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
                });
                return _data;


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

        if _taobao_id:
            key_string = "%s%s" % (_cid, "taobao.com")
        else:
            key_string = "%s%s" % (_cid, "jd.com")

        key = md5(key_string.encode('utf-8')).hexdigest()

        category_id = cache.get(key)
        if category_id is None:
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
        entity.status = Entity.freeze
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
                default = True,
            )
        else:
            Buy_Link.objects.create(
                entity = entity,
                origin_id = _jd_id,
                cid = _cid,
                origin_source = "jd.com",
                link = "http://item.jd.com/%s.html" % _jd_id,
                price = _price,
                default = True,
            )

        return entity


class ReportForms(forms.Form):

    type = forms.ChoiceField(
        label=_("type"),
        choices=Report.TYPE,
        widget=forms.RadioSelect(),
        initial=Report.sold_out,
        # required=False,
    #
    )
    content = forms.CharField(
        label=_("additional remarks"),
        widget=forms.Textarea(attrs={'class':'form-control fs_14 textarea', 'style':"resize: none;", 'rows':'4',}),
        required=False,
    )

    def __init__(self, entity, *args, **kwargs):
        self.entity_cache = entity
        super(ReportForms, self).__init__(*args, **kwargs)

    def save(self, user):
        _content = self.cleaned_data.get('content')
        _type = self.cleaned_data.get('type')
        r = Report(reporter=user, type=_type, comment=_content, content_object=self.entity_cache)

        r.save()
        return r

__author__ = 'edison7500'
