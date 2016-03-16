from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy

from apps.core.models import GKUser , Article , Entity
from apps.shop.models import StorePageBanners, StorePageRecommend
from apps.core.mixins.views import  FilterMixin, SortMixin
from apps.shop.models import Shop

class SellerStoreListView(ListView):
    template_name = 'web/shop/sellers.html'
    context_object_name = 'sellers'

    def get_queryset(self):
        shop_style  = self.get_current_shop_style()
        shop_type = self.get_current_shop_type()
        shops =  Shop.objects.all()
        if shop_style != -1:
            shops = shops.filter(shop_style=shop_style)
        if shop_type  != -1:
            shops = shops.filter(shop_type=shop_type)

        seller_ids = list(shops.values_list('owner__pk', flat=True))
        qs = GKUser.objects.authorized_seller().filter(pk__in=seller_ids)

        return qs

    def get_banners(self):
        return StorePageBanners.objects.filter(status=StorePageBanners.enabled)

    def get_recommends(self):
        return StorePageRecommend.objects.filter(status=StorePageRecommend.enabled)

    def get_current_shop_type(self):

        _shop_type =  self.request.GET.get('shop_type', None)
        try:
            _shop_type = int(_shop_type)
        except  Exception as e:
            _shop_type = -1

        return _shop_type

    def get_current_shop_style(self):
        _shop_style = self.request.GET.get('shop_style', None)
        try:
            _shop_style = int(_shop_style)
        except Exception as  e:
            _shop_style = -1

        return _shop_style

    def get_recent_articles(self):
        sellers_ids = GKUser.objects.authorized_seller().values_list('pk', flat=True)
        recent_articles = Article.objects.published().filter(creator__in=sellers_ids)[:50]
        # entities_recent = Entity.objects.active().filter(user__in=sellers_ids)[:10]
        return recent_articles


    def get_context_data(self, *args, **kwargs):
        context = super(SellerStoreListView, self).get_context_data(*args, **kwargs)
        context['banners'] = self.get_banners()
        context['recommends'] = self.get_recommends()

        context['shop_type_filters'] = Shop.SHOP_TYPE_CHOICES
        context['shop_style_filters'] = Shop.SHOP_STYLE_CHOICES
        context['current_shop_type'] = self.get_current_shop_type()
        context['current_shop_style'] = self.get_current_shop_style()
        context['base_url'] = reverse_lazy('good_store')

        context['recent_articles'] = self.get_recent_articles()

        return context


    pass