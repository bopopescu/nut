from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Note



@check_sign
def detail(request, note_id):


    return SuccessJsonResponse()



__author__ = 'edison7500'
