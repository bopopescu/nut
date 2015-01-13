from apps.core.utils.http import SuccessJsonResponse
from apps.mobile.lib.sign import check_sign
from datetime import datetime


@check_sign
def list(request):

    _timestamp = request.GET.get('timestamp', None)
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))

    _sort_by = request.GET.get('sort', 'novus_time')
    _reverse = request.GET.get('reverse', '0')
    if _reverse == '0':
        _reverse = False
    else:
        _reverse = True

    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))


    return SuccessJsonResponse()


__author__ = 'edison'
