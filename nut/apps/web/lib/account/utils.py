from django.contrib.auth import get_backends, authenticate
from django.contrib.auth import login as auth_login
# from django.contrib.auth import authenticate


def login_without_password(request, user):
    _user = user
    backend = get_backends()[0]
    _user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    auth_login(request, user)


__author__ = 'edison'
