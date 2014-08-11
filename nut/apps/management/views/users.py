from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import GKUser


def list(request, template="management/users/list.html"):

    page = request.GET.get('page', 1)
    user_list = GKUser.objects.all()

    paginator = Paginator(user_list, 30)

    try:
        users = paginator.page(page)
    except InvalidPage:
        users = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(template,
                            {
                                'users':users,
                            },
                            context_instance = RequestContext(request))


def edit(request, user_id, template="management/users/edit.html"):

    try:
        user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    return render_to_response(template,
                                {
                                    'user':user,
                                },
                              context_instance = RequestContext(request))

__author__ = 'edison'
