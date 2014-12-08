from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.forms import PasswordChangeForm
from apps.web.forms.user import UserSettingsForm



def settings(request, template="web/user/settings.html"):
    _user = request.user

    if request.method == 'POST':
        _profile_form = UserSettingsForm(request.POST, user=_user)
        _password_form = PasswordChangeForm(request.POST, user=_user)
    else:
        _profile_form = UserSettingsForm(user=_user)
        _password_form = PasswordChangeForm(user=_user)

    return render_to_response(
        template,
        {
            'user':_user,
            'profile_form':_profile_form,
            'password_form':_password_form,
        },
        context_instance = RequestContext(request),
    )



__author__ = 'edison'
