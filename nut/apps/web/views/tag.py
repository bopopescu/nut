from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView
from apps.tag.models import Tags
# from apps.core.models import Tag, Entity_Tag, Entity, Entity_Like
# from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from django.utils.log import getLogger
from django.views.generic import ListView
log = getLogger('django')



class TagHashView(RedirectView):
    # pass
    pattern_name = 'tag_entities_url'
    # def get

    def get_redirect_url(self, *args, **kwargs):
        _tag = get_object_or_404(Tags, hash=kwargs['hash'])
        return super(TagHashView, self).get(*args, **kwargs)





# def detail(request, hash, template="web/tags/detail.html"):
#     try:
#         _tag = Tag.objects.get(tag_hash = hash)
#     except Tag.DoesNotExist:
#         raise Http404
#
#     return HttpResponseRedirect(reverse('tag_entities_url', args=[_tag.tag]))

    # _page = request.GET.get('page', 1)
    #
    # # inner_qs = Entity_Tag.objects.filter(tag=_tag)
    # # log.info(e)
    # inner_qs = Entity_Tag.objects.filter(tag=_tag).values_list('entity_id', flat=True)
    # _entity_list = Entity.objects.filter(id__in=inner_qs, status=Entity.selection)
    # # log.info(entities)
    # paginator = ExtentPaginator(_entity_list, 24)
    #
    # try:
    #     _entities = paginator.page(_page)
    # except PageNotAnInteger:
    #     _entities = paginator.page(1)
    # except EmptyPage:
    #     raise Http404
    #
    # el = list()
    # if request.user.is_authenticated():
    #     e = _entities.object_list
    #     el = Entity_Like.objects.filter(entity_id__in=list(e), user=request.user).values_list('entity_id', flat=True)
    # log.info(el)
    #
    # return render_to_response(
    #     template,
    #     {
    #         'tag': _tag,
    #         'entities':_entities,
    #         'user_entity_likes': el,
    #     },
    #     context_instance = RequestContext(request),
    # )


# def text_to_detail(request, tag_text):
#     log.info(tag_text)
#     try:
#         _tag = Tag.objects.get(tag = tag_text)
#     except Tag.DoesNotExist:
#         raise Http404
#
#     return HttpResponseRedirect(reverse('web_tag_detail', args=[_tag.tag_hash]))


__author__ = 'edison'
