from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.mobile.forms.account import MobileWeiboSignUpForm, MobileWeiboLoginForm, MobileWeiboLinkForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger

log = getLogger('djang'
                'o')

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
def register_by_weibo(request):
    if request.method == "POST":
        _forms = MobileWeiboSignUpForm(request.POST, request.FILES)
        if _forms.is_valid():
            _user = _forms.save()
            res = {
                'user':_user.v3_toDict(),
                'session': _forms.get_session(),
            }
            return SuccessJsonResponse(res)

        for error in _forms.errors:
            # log.info("error %s" % error)
            return ErrorJsonResponse(status=409, data={
                'type': error,
                'message':'Error',
            })
    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def link_by_weibo(request):

    if request.method == "POST":
        _forms = MobileWeiboLinkForm(request.POST)
        if _forms.is_valid():
            res = _forms.save()
            return SuccessJsonResponse(res)
        log.info(dict(_forms.errors))
        for k, v in _forms.errors.items():
            # log.info("message  %s" % _forms.error_class.as_text(v))
            _message = _forms.error_class.as_text(v)
            return ErrorJsonResponse(status=403, data={
                'type': k,
                'message': _message.replace('*', ''),
            })

    return ErrorJsonResponse(status=400)

__author__ = 'edison'
