from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage


@require_GET
@login_required
def messages(request, template='web/messages/message.html'):
    _user = request.user
    _page = request.GET.get('page', 1)

    message_list = _user.notifications.all()

    paginator = ExtentPaginator(message_list, 10)

    try:
        _messages = paginator.page(_page)
    except PageNotAnInteger:
        _messages = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'messages': _messages
        },
        context_instance = RequestContext(request),
    )


__author__ = 'edison'
