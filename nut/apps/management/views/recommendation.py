from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from apps.core.models import Event, Show_Editor_Recommendation, Editor_Recommendation
from apps.management.forms.editor_recommendation import CreateEditorRecommendForms, EditEditorRecommendForms
from apps.management.decorators import staff_only
# from utils.authority import staff_only

from django.utils.log import getLogger
log = getLogger('django')


@login_required
@staff_only
def list(request, template='management/recommendation/list.html'):

    _show_editor_recommendations = Show_Editor_Recommendation.objects.all()
    _editor_recommendations = Editor_Recommendation.objects.all()
    return render_to_response(
        template,
        {
            'show_editor_recommendations':_show_editor_recommendations,
            'editor_recommendations': _editor_recommendations,
        },
        context_instance=RequestContext(request)
    )


@login_required
@staff_only
def show_list(request, rid, template='management/recommendation/show_list.html'):
    _event = Event.objects.get(pk = rid)
    _show_recommendations = Show_Editor_Recommendation.objects.filter(event_id = rid).order_by('section', '-position')

    return render_to_response(
        template,
        {
            'event': _event,
            'show_recommendations': _show_recommendations,
        },
        context_instance=RequestContext(request),
    )

@login_required
@staff_only
def create(request, event_id = None, template='management/recommendation/create.html'):
    _event_id = event_id

    if request.method == "POST":
        _forms = CreateEditorRecommendForms(request.POST, request.FILES)
        if _forms.is_valid():
            _recommendation = _forms.save()
            return HttpResponseRedirect(reverse('management_recommend_edit', args=[_recommendation.id]))
    else:
        _forms = CreateEditorRecommendForms(
            initial={'event': _event_id},
        )
    return render_to_response(
        template,
        {
            'forms':_forms,
        },
        context_instance=RequestContext(request)
    )


@login_required
@staff_only
def edit(request, event_banner_id, template='management/recommendation/edit.html'):

    try:
        _editor_recommendation = Editor_Recommendation.objects.get(pk = event_banner_id)
    except Editor_Recommendation.DoesNotExist:
        raise Http404

    try:
        show = Show_Editor_Recommendation.objects.get(recommendation = _editor_recommendation)
        event_id = show.event_id
    except Show_Editor_Recommendation.DoesNotExist, e:
        log.error("Error %s" % e.message)
        event_id = None

    data = {
        # 'content_type': _banner.content_type,
        # 'key': _banner.key,
        'link': _editor_recommendation.link,
        'position':_editor_recommendation.position,
        'section': _editor_recommendation.section,
        'event': event_id,
    }

    if request.method == "POST":
        _forms = EditEditorRecommendForms(_editor_recommendation, request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
            return HttpResponseRedirect(reverse('management_event_show_recommendation', args=[event_id]))

        else :
            pass
    else:
        _forms = EditEditorRecommendForms(_editor_recommendation, data=data)


    return render_to_response(
        template,
        {
            'editor_recommendation':_editor_recommendation,
            'forms': _forms,
        },
        context_instance=RequestContext(request)
    )

__author__ = 'edison'
