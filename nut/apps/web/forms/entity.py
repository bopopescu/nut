from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

from apps.core.models import Entity
from apps.core.utils.fetch.taobao import TaoBao

from urlparse import urlparse
import re
from datetime import datetime
from hashlib import md5

log = getLogger('django')


from apps.core.models import Buy_Link


def parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
    return None


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

        if re.search(r"\b(jd|360buy)\.com$", _hostname) != None:
            pass
            # return jd_info(self.request, _link)

        if re.search(r"\b(tmall|taobao|95095)\.(com|hk)$", _hostname) is not None:
            _taobao_id = parse_taobao_id_from_url(_link)
            # log.info(_taobao_id)
            _data = dict()
            try:
                buy_link = Buy_Link.objects.get(origin_id=_taobao_id)
                log.info(buy_link.entity)
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
                }
            return _data



class CreateEntityForm(forms.Form):

    taobao_id = forms.CharField(
        widget=forms.TextInput()
    )
    cid = forms.IntegerField(
        widget=forms.TextInput(),
    )
    shop_nick = forms.CharField(
        widget=forms.TextInput()
    )
    shop_link = forms.URLField(
        widget=forms.URLInput()
    )
    taobao_title = forms.CharField(
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
        _shop_nick = self.cleaned_data.get('shop_nick')
        _brand = self.cleaned_data.get('brand')
        _title = self.cleaned_data.get('taobao_title')
        _cid = self.cleaned_data.get('cid', 300)
        _price = self.cleaned_data.get('price')
        _chief_image_url = self.cleaned_data.get('chief_image_url')
        _images = self.data.getlist('thumb_images')

        # log.info(_chief_image_url)
        _entity_hash = cal_entity_hash(_taobao_id+_title+_shop_nick)

        if _chief_image_url in _images:
            _images.remove(_chief_image_url)

        _images.insert(0, _chief_image_url)

        log.info("images %s" % len(_images))

        entity = Entity(
            user_id=self.request.user.id,
            entity_hash= _entity_hash,
            category_id = 300,
            brand=_brand,
            title=_title,
            price=_price,
            images=_images,
        )

        log.info(entity.images)
        entity.save()
        return entity





__author__ = 'edison7500'
