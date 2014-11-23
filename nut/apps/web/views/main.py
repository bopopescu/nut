from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse


def index(request):


    return HttpResponse("OK")


def selection(request, template='web/main/selection.html'):


    return render_to_response(
        template,
        {

        },

    )


def popular(request, template='web/main/popular.html'):


    return render_to_response(
        template,
        {

        },

    )

__author__ = 'edison'



