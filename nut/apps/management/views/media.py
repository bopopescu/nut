from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from apps.core.utils.image import HandleImage
from apps.core.models import Media
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger


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


def delete(request):
    pass

@csrf_exempt
def upload_image(request):

    if request.method == "POST":
        file =  request.FILES.get('file')
        image = HandleImage(file)
        filename = image.save()

        media =  Media.objects.create(
            file_path = filename,
            content_type = 'image/jpeg',
        )
        return HttpResponse(media.file_url)
    else:
        return HttpResponseBadRequest()

__author__ = 'edison'
