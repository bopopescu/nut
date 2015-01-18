from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.forms.account import MobileUserSignInForm
from apps.mobile.lib.sign import check_sign

from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger

log = getLogger('django')


@csrf_exempt
@check_sign
def login(request):
    if request.method == "POST":
        _forms = MobileUserSignInForm(request=request, data=request.POST)
        log.info(request.POST)
        if _forms.is_valid():
            _forms.login()
            user = _forms.get_user()

            res = dict()
            res['user'] = user.v3_toDict()
            res['session'] = _forms.get_session()
            return SuccessJsonResponse(res)
    else:
        _forms = MobileUserSignInForm(request=request)

    log.info(_forms.errors)

    return ErrorJsonResponse(status=400)


__author__ = 'edison7500'
