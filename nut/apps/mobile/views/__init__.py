from apps.mobile.lib.sign import check_sign
from apps.core.utils.http import SuccessJsonResponse
from apps.core.models import Show_Banner, Banner

from django.utils.log import getLogger

log = getLogger('django')


@check_sign
def homepage(request):

    res = dict()

    innqs = Show_Banner.objects.all().values_list('banner_id', flat=True)
    log.info(innqs)
    banners = Banner.objects.filter(id__in=innqs)

    res['banner'] = []
    for banner in banners:
        res['banner'].append(
            {
                'url':banner.url,
                'img':banner.image_url
            }
        )

    res['config'] = {}
    res['config']['taobao_ban_count'] = 2
    res['config']['url_ban_list'] = ['http://m.taobao.com/go/act/mobile/cloud-jump.html']


    return SuccessJsonResponse(data=res)


__author__ = 'edison7500'
