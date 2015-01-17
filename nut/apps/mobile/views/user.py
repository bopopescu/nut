from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Entity_Tag, GKUser
from django.utils.log import getLogger


log = getLogger('django')


@check_sign
def tag_detail(request, user_id, tag):

    try:
        user = GKUser.objects.get(pk=user_id)
    except GKUser.DoesNotExist:
        return ErrorJsonResponse(status=404)

    tags = Entity_Tag.objects.filter(user_id=user_id, tag__tag=tag)

    # log.info(tags)
    # log.in
    res = dict()
    res['user'] = user.v3_toDict()
    res['entity_list'] = []
    for row in tags:
        entity = row.entity
        res['entity_list'].append(entity.v3_toDict())
        # log.info(entity)

    log.info(res)

    return SuccessJsonResponse(res)


__author__ = 'edison7500'
