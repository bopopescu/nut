from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse

from apps.mobile.forms.account import MobileTaobaoLogin
from apps.mobile.lib.sign import check_sign

# from apps.mobile.models import Session_Key

from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger

log = getLogger('django')



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
def register_by_taobao(request):


    return ErrorJsonResponse(status=400)




__author__ = 'edison7500'

