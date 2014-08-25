from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.log import getLogger

from apps.core.models import GKUser
from apps.core.forms.user import UserForm, GuokuSetPasswordForm, AvatarForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage


log = getLogger('django')


def list(request, template="management/users/list.html"):

    page = request.GET.get('page', 1)
    active = request.GET.get('active', None)
    admin = request.GET.get('admin', None)

    if active == '1':
        user_list = GKUser.objects.active()
    elif active == '0':
        user_list = GKUser.objects.blocked()
    elif active == '-1':
        user_list = GKUser.objects.deactive()
    elif admin:
        user_list = GKUser.objects.admin()
    else:
        user_list = GKUser.objects.all()

    paginator = ExtentPaginator(user_list, 30)

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
        # log.info('change %s', _forms.has_changed())
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



def reset_password(request, user_id, template='management/users/reset_password.html'):

    try:
        _user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = GuokuSetPasswordForm(_user, request.POST)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = GuokuSetPasswordForm(user=_user)

    return render_to_response(
        template,
        {
            'user': _user,
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


def upload_avatar(request, user_id, template='management/users/upload_avatar.html'):

    try:
        _user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    _forms = AvatarForm(user=_user)

    return render_to_response(
        template,
        {
            'user': _user,
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
