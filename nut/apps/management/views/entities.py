from django.shortcuts import render_to_response

def list(request, template = 'management/entities/list.html'):

    return render_to_response(template,
                              )

__author__ = 'edison7500'
