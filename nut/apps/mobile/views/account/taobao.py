from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse

from apps.mobile.forms.account import MobileTaobaoLoginForm, MobileTaobaoSignUpForm
from apps.mobile.lib.sign import check_sign

# from apps.mobile.models import Session_Key

from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger

log = getLogger('django')



@csrf_exempt
@check_sign
def login_by_taobao(request):
    if request.method == "POST":
        _forms = MobileTaobaoLoginForm(request.POST)
        if _forms.is_valid():
            res = _forms.login()
            return SuccessJsonResponse(res)
        return ErrorJsonResponse(status=409, data={
            'type':'taobao_id',
        })
    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def register_by_taobao(request):

    if request.method == "POST":
        log.info(request.POST)
        _forms = MobileTaobaoSignUpForm(data=request.POST, files=request.FILES)
        if _forms.is_valid():
            _user = _forms.save()
            res = {
                'user': _user,
                'session': _forms.get_session()
            }
            return SuccessJsonResponse(res)
        for error in _forms.errors:
            # log.info("error %s" % error)
            return ErrorJsonResponse(status=409, data={
                'type': error,
                'message':'Error',
            })

    return ErrorJsonResponse(status=400)




__author__ = 'edison7500'

