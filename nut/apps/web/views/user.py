from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt

from apps.web.forms.user import UserSettingsForm
from apps.core.utils.http import JSONResponse
from apps.core.utils.image import HandleImage

from django.utils.log import getLogger

log = getLogger('django')


def settings(request, template="web/user/settings.html"):
    _user = request.user

    if request.method == 'POST':
        _profile_form = UserSettingsForm(_user, request.POST)
        if _profile_form.is_valid():
            _profile_form.save()
        # _password_form = PasswordChangeForm(request.POST, user=_user)
    else:
        data = {
            'nickname': _user.profile.nickname,
            'email': _user.email,
            'bio': _user.profile.bio,
            'location': _user.profile.location,
            'city': _user.profile.city,
            'gender': _user.profile.gender,
            'website': _user.profile.website,
        }
        # log.info(data['city'])
        _profile_form = UserSettingsForm(user=_user, initial=data)
        # _password_form = PasswordChangeForm(user=_user)

    return render_to_response(
        template,
        {
            'user':_user,
            'profile_form':_profile_form,
            # 'password_form':_password_form,
        },
        context_instance = RequestContext(request),
    )


@csrf_exempt
def upload_avatar(request):
    _user = request.user
    if request.method == 'POST':
        # log.info(request.FILES)
        _file_obj = request.FILES.get('avatar_img')
        _image = HandleImage(_file_obj)
        _image.resize(300, 300)
        avatar_file_name  = _image.save(square=True)
        _user.profile.avatar = avatar_file_name
        _user.profile.save()
        log.info(_user.profile.avatar_url)
        return  JSONResponse(status=200, data={'avatar_url':_user.profile.avatar_url})

    return

__author__ = 'edison'
