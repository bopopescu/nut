from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from apps.core.utils.image import HandleImage,LimitedImage
from apps.core.utils.http import ErrorJsonResponse, SuccessJsonResponse
from apps.core.models import Media
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.management.decorators import staff_only, writers_only

from django.utils.log import getLogger
log = getLogger('django')

@login_required
@staff_only
def list(request, template="management/media/list.html"):

    _page = request.GET.get('page', 1)
    medium_list = Media.objects.all()

    paginator = ExtentPaginator(medium_list, 30)

    try:
        _media = paginator.page(_page)
    except PageNotAnInteger:
        _media = paginator.page(1)
    except EmptyPage:
        raise  Http404

    return render_to_response(
        template,
        {
            'media': _media
        },
        context_instance = RequestContext(request)
    )


@csrf_exempt
@login_required
@staff_only
def delete(request):
    if request.method == "POST":
        mid = request.POST.get('mid', None)

        try:
            medium = Media.objects.get(pk = mid)
            medium.delete()
        except Media.DoesNotExist:
            raise Http404

        return SuccessJsonResponse(data={'msg':'success'})
    else:
        return ErrorJsonResponse(status=400)


@csrf_exempt
@login_required
@writers_only
def upload_image(request):

    if request.method == "POST":
        log.info('img upload begin----')

        file = request.FILES.get('file')
        image = LimitedImage(file)
        log.info('image handeled and returned')
        log.info(image)
        filename = image.save()
        log.info('image saved -----')
        log.info(filename)

        media =  Media.objects.create(
            file_path = filename,
            content_type = image.content_type,
            creator = request.user
        )
        log.info(media)
        return HttpResponse(media.file_url)
    else:
        return HttpResponseBadRequest()

__author__ = 'edison'
