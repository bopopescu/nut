from random import shuffle

from django.views.generic import DetailView
from django.core.cache import cache

from apps.offline_shop.models import Offline_Shop_Info
from apps.core.models import Entity, Article

entities_hashs = [
    ['3e9788ce',
     'f7fc045c',
     '999522e3',
     '4b0a4460',
     '56ff23a9',
     'aae3d211',
     '496e5041',
     '7893125c',
     '2b3aa24d',
     '767e12f9',
     'ff88ad68',
     '9cbfd9bc',
     'd10ae55e',
     '00881c27',
     '5a90e5e9',
     'b73fe466',
     '2ecf02f6',
     '29f23603',
     '418f9cbd',
     '0b587e2f',
     'f687f7b0',
     '097e0319',
     'd7792614',
     'b320f7ed',
     'ca429d59',
     '8d6f38e9',
     '3dc6381e',
     'd7a8e799',
     'faff856d',
     'bf752979',
     'cdaa9431',
     'c161e6ed',
     '36675e44',
     'fe0cbdc5',
     'ece64417'
     ],
    ['3b257bf4',
     'b1840f82',
     '136327af',
     '1144afa1',
     '34c6b61c',
     '8240630d',
     '8418362e',
     '3402cc9d',
     '6e3fe109',
     'ab975b0c',
     '6836c28a',
     'ae82275c',
     '17545805',
     '76824edf',
     '435c9221',
     '9a5a92b6',
     '5c646801'
     ],
    ['dfad0c16',
     'b1840f82',
     '3f4c2736',
     '34c6b61c',
     'd3208043',
     '0e641501',
     'fc58663e',
     '8240630d',
     '8418362e',
     'f6453176',
     '9a5a92b6',
     '4c16550a',
     '5c646801',
     'c57a88e7',
     '708cfe53',
     'd3439f7b'
     ]
]


articles = [
    [
        '134060',
        '244'
    ],
    [
        '134060',
        '110'
        '702',
        '320',
        '65'
    ],
    [
        '135527'
    ]
]


class OfflineShopDetailView(DetailView):
    template_name = 'web/offline_shop/offline_detail.html'
    pk_url_kwarg = 'offline_shop_id'
    model = Offline_Shop_Info
    context_object_name = 'offline_shop'

    def get_articles(self):
        offline_shop_id = int(self.get_shop_id())
        sel_articles = articles[offline_shop_id - 1]
        shuffle(sel_articles)
        return Article.objects.filter(pk__in=sel_articles[:3])

    def get_shop_id(self):
        return self.kwargs.get('offline_shop_id')

    def get_entities(self):
        key = 'offlineshop:entities:cache' + self.get_shop_id()
        entities = cache.get(key)
        if entities is None:
            offline_shop_id = int(self.get_shop_id())
            entities = Entity.objects.filter(entity_hash__in=entities_hashs[offline_shop_id - 1])
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
        context_data['offline_shop_cover'] = context_data['object'].images[0]
        return context_data
