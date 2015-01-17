from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Entity_Tag


@check_sign
def tag_detail(request, user_id, tag):

    tags = Entity_Tag.objects.filter(user_id=user_id, tag__)

    return SuccessJsonResponse()


__author__ = 'edison7500'
