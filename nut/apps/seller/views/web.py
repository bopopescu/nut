# coding=utf-8

import random
import urllib
from braces.views import AjaxResponseMixin
from django.http import Http404
from django.utils.encoding import smart_str
from django.views.generic import TemplateView, ListView, RedirectView
from apps.seller.models import Seller_Profile
from apps.core.models import Entity, Article, GKUser, Selection_Article
from apps.tag.models import Tags, Content_Tags


class TrendRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'year_store_2016'

class Seller2015RedirectView(RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'year_store_2015'

class SellerView(TemplateView):
    template_name = 'web/seller/web_seller.html'

    def get_base_sellers(self):
        return Seller_Profile.objects.seller_2015()

    def get_seller_by_business_section(self, section):
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
    u'FASHION': [2025777, 2025778, 1995042, 2025779, 2006725, 2025780],
    u'FOOD': [2025782, 2025783, 2025786, 2025787, 2025788],
    u'CULTURE': [2025789, 2025790, 1993297, 2025791, 2025792],
    u'LIFESTYLE': [2025794, 1992722, 2025795, 2025796, 2025797, 2023605, 2003684],
    u'TECH': [2025798, 2025799, 2025800],
    u'BEAUTY': [2025804, 2025801, 2025802, 2025803]
}

topic_tags ={
    u'进击的扁平化': u'这些品牌换了 logo，除了更扁平，还意味着什么？',
    u'科技生活零距离': u'VR 元年，全民直播，科技正在成为人体的一部分',
    u'消费升级': u'人人都谈消费升级的年代，这些事儿正在影响你的花钱质量。',
    u'吃得更讲究': u'米其林都来中国了，「吃货崇拜」这病还会越来越流行。',
    u'开店新时髦': u'实体店唱衰的时代，只开几天的店铺成了新时髦。',
    u'城市生活可能性': u'这些事情话你知，好的生活有太多可能了。',
    u'这杯咖啡必须买': u'连锁制霸的时代早就过去了，喝咖啡和卖咖啡正在变得越来越有看头。',
    u'你我他': u'2016，这些名字值得记住。',
    u'这些单品不好买': u'我们没法替你排队，只好替你总结。',
    u'霓虹新印象': u'奥运会东京接棒，此时以及未来的日本，会是什么样？'
}

column_tag_name = '年度专栏2016'


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

    def get_topic_tags(self):
        tag_names = topic_tags.keys()
        tag_list = list(Tags.objects.filter(name__in=tag_names))
        for tag in tag_list:
            tag.info = topic_tags[tag.name]
        return tag_list

    def get_column_articles(self):
        c_tag = Tags.objects.filter(name=column_tag_name)
        if c_tag.exists():
            artilcle_ids = list(Content_Tags.objects.filter(target_content_type_id=31, tag__name=column_tag_name)\
                                        .values_list('target_object_id', flat=True))
            return Article.objects.filter(pk__in=artilcle_ids[:10])
        else:
            return []

    def get_topic_articles(self):
        tags = self.get_topic_tags()
        article_ids = list(Content_Tags.objects.filter(target_content_type_id=31, tag__in=tags)\
                                  .values_list('target_object_id', flat=True))
        random.shuffle(article_ids)
        return Article.objects.filter(pk__in=article_ids[:3])


class ShopsView(Base2016SellerView):
    template_name = 'web/seller/web_seller_2016_shops.html'


class OpinionsView(TemplateView):
    template_name = 'web/seller/web_seller_2016_opinions.html'
    def get_context_data(self, *args, **kwargs):
        context = super(OpinionsView, self).get_context_data(*args, **kwargs)
        context['fashion_writer'] = self.get_writer_by_category(u'FASHION')
        context['food_writer'] = self.get_writer_by_category(u'FOOD')
        context['culture_writer'] = self.get_writer_by_category(u'CULTURE')
        context['life_writer'] = self.get_writer_by_category(u'LIFESTYLE')
        context['tech_writer'] = self.get_writer_by_category(u'TECH')
        context['beauty_writer'] = self.get_writer_by_category(u'BEAUTY')
        return context

    def get_writer_by_category(self, cate):
        w_list = writer_list[cate]
        return GKUser.objects.filter(pk__in=w_list)


class ColumnsView(TemplateView):
    template_name = 'web/seller/web_seller_2016_columns.html'
    def get_context_data(self, *args, **kwargs):
        context = super(ColumnsView, self).get_context_data(*args, **kwargs)
        context['articles'] = self.get_column_articles()
        return context

    def get_column_articles(self):
        c_tag = Tags.objects.filter(name=column_tag_name)
        if c_tag.exists():
            artilcle_ids = Content_Tags.objects.filter(target_content_type_id=31, tag__name=column_tag_name)\
                                        .values_list('target_object_id', flat=True)
            return Article.objects.filter(pk__in=artilcle_ids)
        else:
            return []


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

    def get_article_tag(self):
        tag_name =  self.kwargs.get('tag_name')
        if tag_name is None:
            return None
        return urllib.unquote(str(tag_name)).decode('utf-8')

    def get_context_data(self,*args, **kwargs):
        context = super(TopicArticlesView, self).get_context_data(*args, **kwargs)
        context['articles'] = self.get_articles()
        context['topic_tags'] = self.get_all_topic_tags()
        context['current_tag_name'] = self.get_article_tag()
        return context

    def get_articles(self):
        tag_name = self.get_article_tag()
        if tag_name is None:
            return self.get_all_topic_articles()
        else:
            return self.get_topic_articles(tag_name)


    def get_all_topic_articles(self):
        tags = self.get_all_topic_tags()
        article_ids = list(Content_Tags.objects.filter(target_content_type_id=31, tag__in=tags)\
                                  .values_list('target_object_id', flat=True))
        # random.shuffle(article_ids)
        return Article.objects.filter(pk__in=article_ids)

    def get_all_topic_tags(self):
        tag_names = topic_tags.keys()
        tag_list = Tags.objects.filter(name__in=tag_names)
        for tag in tag_list:
            tag.info = topic_tags[tag.name]
        return tag_list

    def get_topic_articles(self, tag_name):
        tag_list = list(Tags.objects.filter(name=smart_str(tag_name)))
        article_ids = list(Content_Tags.objects.filter(target_content_type_id=31, tag__in=tag_list)\
                                  .values_list('target_object_id', flat=True))
        return Article.objects.filter(pk__in=article_ids)










