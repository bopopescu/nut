import random

from django.views.generic import TemplateView, ListView
from apps.seller.models import Seller_Profile
from apps.core.models import Entity, Article, GKUser, Selection_Article
from apps.tag.models import Tags


class SellerView(TemplateView):
    template_name = 'web/seller/web_seller.html'

    def get_base_sellers(self):
        return Seller_Profile.objects.seller_2015()

    def get_seller_by_business_section(self,section):
        return self.get_base_sellers().ordered_profile().filter(business_section=section).select_related('related_article__url')

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

        context['sellers'] = self.get_base_sellers().ordered_all_profile()
        context['star_range'] = xrange(5)

        return context


class Base2016SellerView(SellerView):
    def get_base_sellers(self):
        return Seller_Profile.objects.seller_2016()


writer_list = {
    'FASHION ': [2025777, 2025778, 1995042, 2025779, 2006725, 2025780],
    'FOOD': [2025782, 2025783, 2025786, 2025787, 2025788],
    'CULTURE': [2025789, 2025790, 1993297, 2025791, 2025792],
    'LIFESTYLE': [2025794, 1992722, 2025795, 2025796, 2025797, 2023605, 2003684],
    'TECH': [2025798, 2025799, 2025800],
    'BEAUTY': [2025804, 2025801, 2025802, 2025803]
}

topic_tags = ['']


class NewSellerView(TemplateView):
    template_name = 'web/seller/web_seller_2016.html'

    def get_base_sellers(self):
        return Seller_Profile.objects.seller_2016()

    def get_context_data(self, **kwargs):
        context = {}
        context['sellers'] = self.get_top_sellers()
        context['writers'] = self.get_top_writers()
        context['topic_tags'] = self.get_topic_tags()
        context['opinions_tags'] = self.get_get_opinions_tags()
        context['opinion_articles'] = self.get_opinions_articles()
        context['column_articles'] = self.get_column_articles()
        context['top_article_tags'] = Tags.objects.top_article_tags()
        return context

    def get_top_sellers(self):
        return Seller_Profile.objects.random_sellers()

    def get_all_writers(self):
        writers_ids = self.get_writers_ids()
        return GKUser.objects.filter(pk__in=writers_ids)

    def get_writers_ids(self):
        writers_ids = []
        for key, value in writer_list.iteritems():
            writers_ids += value
        return writers_ids

    def get_top_writers(self):
        writers_ids = self.get_writers_ids()
        ids = random.sample(writers_ids, 10)
        return GKUser.objects.filter(pk__in=ids)


    def get_get_opinions_tags(self):
        pass

    def get_column_articles(self):
        pass

    def get_opinions_articles(self):
        pass

    def get_topic_tags(self):
        pass


class ShopsView(Base2016SellerView):
    template_name = 'web/seller/web_seller_2016_shops.html'


class OpinionsView(SellerView):
    template_name = 'web/seller/web_seller_2016_opinions.html'


class ColumnsView(SellerView):
    template_name = 'web/seller/web_seller_2016_columns.html'


class TopicsView(SellerView):
    template_name = 'web/seller/web_seller_2016_topics.html'
    model = Selection_Article
    context_object_name = 'selection_articles'

    def get_context_data(self, **kwargs):
        context = super(TopicsView, self).get_context_data(**kwargs)
        context['top_article_tags'] = Tags.objects.top_article_tags()

        return context


class TopicArticlesView(ListView):
    http_method_names = ['get']
    template_name = 'web/seller/web_seller_2016_topics.html'
    model = Selection_Article
    context_object_name = 'selection_articles'

    def get_context_data(self, **kwargs):
        context = super(TopicArticlesView, self).get_context_data(**kwargs)
        context['top_article_tags'] = Tags.objects.top_article_tags()

        return context










