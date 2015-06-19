from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.v4.forms.accounts.baichuan import BaichuanSignInForm

from apps.mobile.lib.sign import check_sign
from django.views.decorators.csrf import csrf_exempt

from django.utils.log import getLogger

log = getLogger('django')


@csrf_exempt
@check_sign
def login(request):
    code = 200
    if 'iPhone' in request.META['HTTP_USER_AGENT'] or 'iPad' in request.META['HTTP_USER_AGENT']:
        code = 409

    if request.method == "POST":
        log.info(request.POST)
        _form = BaichuanSignInForm(request.POST)
        if _form.is_valid():
            res = _form.login()

            return SuccessJsonResponse(data=res)

        for k, v in dict(_form.errors).items():
            log.info(v.as_text().split('*'))
            error_msg = v.as_text().split('*')[1]
            return ErrorJsonResponse(status=code, data={
                'type': k,
                'message': error_msg.lstrip(),
            })

    return ErrorJsonResponse(status=400)

__author__ = 'edison'
