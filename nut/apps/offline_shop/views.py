from random import shuffle

from django.views.generic import DetailView
from django.core.cache import cache

from apps.offline_shop.models import Offline_Shop_Info
from apps.core.models import Entity, Article

entities_hashs = [

    '3b257bf4',
    '136327af',
    '1144afa1',
    '34c6b61c',
    '8240630d',
    '8418362e',
    '0e641501',

    '3402cc9d',
    '6e3fe109',
    'ab975b0c',
    'f6453176'

    '708cfe53',
    '5c646801',
    '9a5a92b6',
    'dfad0c16',

    '76824edf',
    '8fad39f7',
    '17545805',

    '2a1599fa',
]


articles = [
    '110',
    '134058',
    '6858',
    '51962',
    '134059',
    '5482',
    '65',
    '320'
]


class OfflineShopDetailView(DetailView):
    template_name = 'web/offline_shop/offline_detail.html'
    pk_url_kwarg = 'offline_shop_id'
    model = Offline_Shop_Info
    context_object_name = 'offline_shop'

    def get_articles(self):
        sel_articles = articles[:]
        shuffle(sel_articles)
        return Article.objects.filter(pk__in=sel_articles[:3])

    def get_shop_id(self):
        return self.kwargs.get('offline_shop_id')

    def get_entities(self):
        key = 'offlineshop:entities:cache' + self.get_shop_id()
        entities = cache.get(key)
        if entities is None:
            entities = Entity.objects.filter(entity_hash__in=entities_hashs)
            entities = list(entities)
            shuffle(entities)
            cache.set(key, entities, timeout=3600)
        else:
            return entities

    def get_context_data(self, **kwargs):
        context_data = super(OfflineShopDetailView, self).get_context_data(**kwargs)
        context_data['current_user'] = context_data['object'].shop_owner
        context_data['entities'] = self.get_entities()
        context_data['articles'] = self.get_articles()
        return context_data
