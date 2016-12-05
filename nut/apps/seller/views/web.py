from django.views.generic import TemplateView, ListView
from apps.seller.models import Seller_Profile
from apps.core.models import Entity, Article , GKUser



class SellerView(TemplateView):

    template_name = 'web/seller/web_seller.html'

    def get_seller_by_business_section(self,section):
        return Seller_Profile.objects.ordered_profile().filter(business_section=section).select_related('related_article__url')

    def get_seller_entities(self, seller_queryset):
        article_list = Article.objects.filter(related_seller__in=seller_queryset)
        entities = Entity.objects.filter(related_articles__in=article_list)
        return entities

    def get_seller_section_entities(self, section):
        seller_queryset = self.get_seller_by_business_section(section)
        return self.get_seller_entities(seller_queryset)

    def get_context_data(self, **kwargs):
        context = super(SellerView, self).get_context_data(**kwargs)

        context['food_sellers'] = self.get_seller_by_business_section(Seller_Profile.food)
        context['food_entities'] = self.get_seller_section_entities(Seller_Profile.food)

        context['culture_sellers'] = self.get_seller_by_business_section(Seller_Profile.culture)
        context['culture_entities'] = self.get_seller_section_entities(Seller_Profile.culture)


        context['cloth_sellers'] = self.get_seller_by_business_section(Seller_Profile.cloth)
        context['cloth_entities'] = self.get_seller_section_entities(Seller_Profile.cloth)


        context['life_sellers'] = self.get_seller_by_business_section(Seller_Profile.life)
        context['life_entities'] = self.get_seller_section_entities(Seller_Profile.life)

        context['blank_sellers'] = self.get_seller_by_business_section(Seller_Profile.blank)
        context['blank_entities'] = self.get_seller_section_entities(Seller_Profile.blank)

        context['sellers'] = Seller_Profile.objects.ordered_all_profile()
        context['star_range'] = xrange(5)

        return context


class NewSellerView(SellerView):
    template_name = 'web/seller/web_seller_2016.html'




