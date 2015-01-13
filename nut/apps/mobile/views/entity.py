from apps.core.utils.http import SuccessJsonResponse
from apps.mobile.lib.sign import check_sign


@check_sign
def list(request):



    return SuccessJsonResponse()


__author__ = 'edison'
