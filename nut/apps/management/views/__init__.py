from django.shortcuts import render_to_response


def dashboard(request, template='management/dashboard.html'):


    return render_to_response(template)


__author__ = 'edison7500'
