#coding=utf-8
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
# from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext_lazy as _
from django.utils.feedgenerator import Rss201rev2Feed
# from django.shortcuts import get_object_or_404
# from xml.sax.saxutils import escape

from apps.core.models import Selection_Entity, Selection_Article

from django.utils.html import strip_tags, escape

from datetime import datetime


from xml.sax.saxutils import XMLGenerator

class SimplerXMLGenerator(XMLGenerator):
    def addQuickElement(self, name, contents=None, attrs=None, escape=False):
        "Convenience method for adding an element with no children"
        if attrs is None: attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            if escape:
                self.characters(contents)
            else:
                if not isinstance(contents, unicode):
                    contents = unicode(contents, self._encoding)
                self._write(contents)
        self.endElement(name)


class CustomFeedGenerator(Rss201rev2Feed):
    mime_type = 'application/xml; charset=utf-8'
    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u"image", item['image'])
        # handler.addQuickElement(u"short_description", item['short_description'])

class ArticlesFeedGenerator(Rss201rev2Feed):

    mime_type = 'application/xml; charset=utf-8'
    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement("rss", self.rss_attributes())
        handler.startElement("channel", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement("rss")


    def rss_attributes(self):
        attrs = super(ArticlesFeedGenerator, self).rss_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        attrs['xmlns:georss'] = 'http://www.georss.org/georss'
        attrs['xmlns:dc'] ="http://purl.org/dc/elements/1.1/"
        return attrs

    # def add_root_elements(self, handler):
    #     super(ArticlesFeedGenerator, self).add_root_elements(handler)
    #     print self.feed

    def add_item_elements(self, handler, item):
        super(ArticlesFeedGenerator, self).add_item_elements(handler, item)

        # if item['content_encoded'] is not None:
            # handler.strat
        # content = '<![CDATA[' +item['content'] + ']]>'
        # handler.addQuickElement(u'content:encoded', item['content_encoded'])

        if item['content_encoded'] is not None:
            handler.addQuickElement(u'content:encoded', item['content_encoded'], escape=False)
        # if item['description_encoded'] is not None:
        #     handler.addQuickElement(u'description', item['description_encoded'], escape=True)
            # handler.startElement(u'content:encoded', {})
            # handler._write(item['content_encoded'])
            # handler.endElement(u'content:encoded')


class SelectionFeeds(Feed):
    feed_type = CustomFeedGenerator

    title = _("live different")
    link = '/selected/'
    description = _('guoku selection desc')

    description_template = "web/feeds/selection_description.html"

    def items(self):
        return Selection_Entity.objects.published().filter(pub_time__lt = datetime.now())[:60]
        # return NoteSelection.objects(post_time__lt = datetime.now())[:60]

    def item_title(self, item):
        return item.entity

    def item_link(self, item):
        return reverse('web_entity_detail', args=[item.entity.entity_hash])

    def item_description(self, item):
        return item.top_note.note

    def item_author_name(self, item):
        return item.entity.top_note.user.profile.nickname

    def item_pubdate(self, item):
        # _note_id = item.note_id
        # _note_context = Note(_note_id).read()
        # return _note_context['post_time']
        return item.pub_time

    def item_extra_kwargs(self, item):
        # _entity_id = item.entity_id
        # _entity_context = Entity(_entity_id).read()
        return {'image':item.entity.chief_image}


class ArticlesFeeds(Feed):
    feed_type = ArticlesFeedGenerator
    title = u'图文频道>>果库|精英消费者南'
    link = "/articles/"
    author_email = "hi@guoku.com"
    feed_copyright = "2010-2015 果库. All rights reserved."
    description = '果库消费图文汇集全网秉持理想生活哲学的消费类文章，开拓精英视野与生活想象，涵盖品牌相关报道、卖家创业者专访、潮流资讯、消费见解主张、生活场景清单、购物经验心得分享等。'


    # description_template = "web/feeds/article_description.html"

    # def get_object(self, request, *args, **kwargs):
    #     return getattr(get_object_or_404)

    def items(self):
        return Selection_Article.objects.published().order_by('-pub_time')[0:30]

    def item_title(self, item):
        return escape(item.article.title)

    def item_link(self, item):
        return reverse('web_article_page', args=[item.article.pk])+'?from=feed'

    def item_author_name(self, item):
        return escape(item.article.creator.profile.nick)

    def item_pubdate(self, item):
        return item.pub_time

    def item_description(self, item):
        content = strip_tags(item.article.content)
        # content = strip_tags(item.article.bleached_content)
        desc = content.split(u'。')
        # return "<![CDATA[%s]]>" % (desc[0] + u'。')
        return escape(desc[0] + u'。')

    def item_extra_kwargs(self, item):
        # extra = super(ArticlesFeeds, self).item_extra_kwargs(item)
        extra = {
                # 'content_encoded': "<![CDATA[%s]]>" % item.article.content,
                'content_encoded': "<![CDATA[%s]]>" % item.article.bleached_content,
                # 'content_encoded': "<![CDATA[%s]]>" % u'<p>test</p>',
                }
        return extra


__author__ = 'edison7500'
