from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import GKUser


def list(request, template="management/users/list.html"):

    user_list = GKUser.objects.all()



    return render_to_response(template,
                            {

                            },
                            context_instance = RequestContext(request))

__author__ = 'edison'
