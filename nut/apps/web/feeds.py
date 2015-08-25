#coding=utf-8
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
# from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext_lazy as _
from django.utils.feedgenerator import Rss201rev2Feed

from apps.core.models import Selection_Entity, Selection_Article
from django.utils.html import strip_tags

# from base.models import NoteSelection
# from base.entity import Entity
# from base.note import Note
# from base.user import User
from datetime import datetime

class CustomFeedGenerator(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u"image", item['image'])
        # handler.addQuickElement(u"short_description", item['short_description'])

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
        # _entity_id = item.entity.title
        # _entity_context = Entity(_entity_id).read()
        if len(item.entity.brand) > 0:
            return "%s - %s" % (item.entity.brand, item.entity.title)
        return item.entity.title

    def item_link(self, item):
        # _entity_id = item.entity_id
        # _entity = Entity.objects.get(pk = _entity_id)
        # _entity_context = Entity(_entity_id).read()
        # return "/detail/%s/" % _entity_context['entity_hash']
        return reverse('web_entity_detail', args=[item.entity.entity_hash])

    def item_description(self, item):
        return item.top_note.note
    #     _note_id = item.note_id
    #     _note_context = Note(_note_id).read()
    #     return _note_context['content']

    def item_author_name(self, item):
        # _note_id = item.note_id
        # _note_context = Note(_note_id).read()
        # _creator_context = User(_note_context['creator_id']).read()
        # return _creator_context['nickname']
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
    feed_type = Rss201rev2Feed

    title = u'果库 － 精英消费者南'
    link = "/articles/"
    description = _('精英消费指南')

    description_template = "web/feeds/article_desc.html"

    def items(self):
        return Selection_Article.objects.published().order_by('-pub_time')[0:30]

    def item_title(self, item):
        return item.article.title

    def item_link(self, item):
        return reverse('web_article_page', args=[item.article.pk])

    def item_author_name(self, item):
        return item.article.creator.profile.nick

    def item_pubdate(self, item):
        return item.pub_time

    def item_description(self, item):
        return strip_tags(item.article.content)

    # def item_extra_kwargs(self, item):
    #     return {'image':item.article.cover_url}

    def get_context_data(self, **kwargs):
        context = super(ArticlesFeeds, self).get_context_data(**kwargs)
        return context
        # return con


__author__ = 'edison7500'
