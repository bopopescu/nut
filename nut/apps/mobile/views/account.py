from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.forms.account import MobileUserSignInForm, MobileUserSignUpForm, MobileUserSignOutForm, MobileWeiboLoginForm, MobileTaobaoLogin
from apps.mobile.lib.sign import check_sign

# from apps.mobile.models import Session_Key

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
            _user = _forms.get_user()

            res = {
                'user': _user.v3_toDict(),
                'session': _forms.get_session()
            }
            return SuccessJsonResponse(res)
    else:
        _forms = MobileUserSignInForm(request=request)

    log.info(_forms.errors)
    for error in _forms.errors:
            # log.info("error %s" % error)
        return ErrorJsonResponse(status=400, data={
            'type': 'email',
            'message': 'Error',
        })

    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def register(request):
    if request.method == "POST":
        _forms = MobileUserSignUpForm(request=request, data=request.POST)
        log.info(request.POST)
        if _forms.is_valid():
            _user = _forms.save()
            log.info("user user %s" % _user)
            res = {
                'user':_user.v3_toDict(),
                'session': _forms.get_session()
            }
            return SuccessJsonResponse(res)
        # log.info(_forms.errors)
        for error in _forms.errors:
            # log.info("error %s" % error)
            return ErrorJsonResponse(status=409, data={
                'type': error,
                'message':'Error',
            })

    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def logout(request):
    # _req_uri = request.get_full_path()
    if request.method == "POST":
        _forms = MobileUserSignOutForm(request.POST)
        if _forms.is_valid():
            res = _forms.logout()
            return SuccessJsonResponse({ 'success': '1' })

    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def login_by_weibo(request):
    if request.method == "POST":
        _forms = MobileWeiboLoginForm(request.POST)
        if _forms.is_valid():
            res = _forms.login()
            return SuccessJsonResponse(res)
        return ErrorJsonResponse(status=409, data={
            'type':'sina_id',
        })
    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def login_by_taobao(request):
    if request.method == "POST":
        _forms = MobileTaobaoLogin(request.POST)
        if _forms.is_valid():
            res = _forms.login()
            return SuccessJsonResponse(res)
        return ErrorJsonResponse(status=409, data={
            'type':'taobao_id',
        })
    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def apns_token(request):

    log.info(request.POST)
    return SuccessJsonResponse()

__author__ = 'edison7500'
