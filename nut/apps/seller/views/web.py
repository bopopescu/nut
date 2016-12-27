# coding=utf-8

import random

from django.http import Http404
from django.views.generic import TemplateView, ListView
from apps.seller.models import Seller_Profile
from apps.core.models import Entity, Article, GKUser, Selection_Article
from apps.tag.models import Tags, Content_Tags


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

topic_tags ={
    '进击的扁平化':'这些品牌换了 logo，除了更扁平，还意味着什么？',
    '科技生活零距离':'VR 元年，全民直播，科技正在成为人体的一部分',
    '消费升级':'人人都谈消费升级的年代，这些事儿正在影响你的花钱质量。',
    '吃得更讲究':'米其林都来中国了，「吃货崇拜」这病还会越来越流行。',
    '开店新时髦': '实体店唱衰的时代，只开几天的店铺成了新时髦。',
    '城市生活可能性':'这些事情话你知，好的生活有太多可能了。',
    '这杯咖啡必须买':'连锁制霸的时代早就过去了，喝咖啡和卖咖啡正在变得越来越有看头。',
    '你我他':'2016，这些名字值得记住。',
    '这些单品不好买':'我们没法替你排队，只好替你总结。',
    '霓虹新印象':'奥运会东京接棒，此时以及未来的日本，会是什么样？'
}

column_tag_name = '专栏2016'


class NewSellerView(TemplateView):
    template_name = 'web/seller/web_seller_2016.html'

    def get_base_sellers(self):
        return Seller_Profile.objects.seller_2016()

    def get_context_data(self, **kwargs):
        context = {}
        context['sellers'] = self.get_top_sellers()
        context['writers'] = self.get_top_writers()
        context['topic_tags'] = self.get_topic_tags()
        context['topic_articles'] = self.get_topic_articles()
        context['column_articles'] = self.get_column_articles()
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




    def get_opinions_articles(self):
        pass

    def get_topic_tags(self):
        tag_names = topic_tags.keys()
        tag_list = Tags.objects.filter(name__in=tag_names)
        for tag in tag_list:
            tag.info = topic_tags[tag.name]
        return tag_list

    def get_column_articles(self):
        c_tag = Tags.objects.filter(name=column_tag_name)
        if c_tag.exists():
            artilcle_ids = Content_Tags.objects.filter(target_content_type_id=31, tag__name=column_tag_name)\
                                        .values_list('target_object_id', flat=True)
            return Article.objects.filter(pk__in=artilcle_ids)
        else:
            raise Http404

    def get_topic_articles(self):
        tags = self.get_topic_tags()
        article_ids = Content_Tags.objects.filter(target_content_type_id=31, tag__in=tags)\
                                  .values_list('target_object_id', flat=True)
        random.shuffle(article_ids)
        return Article.objects.filter(pk__in=article_ids)


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










