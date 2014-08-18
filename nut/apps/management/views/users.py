from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import GKUser
from apps.core.forms.user import UserForm


def list(request, template="management/users/list.html"):

    page = request.GET.get('page', 1)
    active = request.GET.get('active', None)
    admin = request.GET.get('admin', None)

    if active:
        user_list = GKUser.objects.active()
    elif admin:
        user_list = GKUser.objects.admin()
    else:
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
                                'active':active,
                                'admin':admin,
                            },
                            context_instance = RequestContext(request))


def edit(request, user_id, template="management/users/edit.html"):

    try:
        user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    data = {
        'user_id':user.pk,
        'email':user.email,
        'nickname': user.profile.nickname,
        'is_active':user.is_active,
        'is_admin':user.is_admin,
        'gender': user.profile.gender,
        'bio': user.profile.bio,
        'website': user.profile.website,
    }

    if request.method == 'POST':
        _forms = UserForm(request.POST, initial=data)
        if _forms.is_valid():
            _forms.save()

    else:
        _forms = UserForm(initial=data)

    return render_to_response(template,
                                {
                                    'user':user,
                                    'forms':_forms,
                                },
                              context_instance = RequestContext(request))

__author__ = 'edison'
