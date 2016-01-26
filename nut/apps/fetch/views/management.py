from django.views.generic import View, ListView
from django.http import HttpResponse
from braces.views import  UserPassesTestMixin
from django.shortcuts import redirect

from apps.fetch.models import SogouCookies


# todo add permission mixin

class AddCookieView(UserPassesTestMixin, View):

    def test_func(self, user):
        return user.is_staff

    def get(self, *args, **kwargs):
        cookie_string = self.request.GET.get('cookie', 'not found')
        try:
            cookie = SogouCookies.objects.get(cookie_string=cookie_string)
        except SogouCookies.DoesNotExist as e:
        #     good create
            cookie = SogouCookies.objects.create(cookie_string=cookie_string)
            cookie.save()
            return redirect('management_cookie_list')

        except SogouCookies.MultipleObjectsReturned:
            return HttpResponse('multiple returned')

        return  HttpResponse('Already Exist : ' + cookie_string)

# javascript:window.open('http://127.0.0.1:9766/management/fetch/addcookie/?cookie=' +encodeURIComponent(document.cookie)+ ' ')


class CookieListView(UserPassesTestMixin, ListView):

    model = SogouCookies
    template_name = 'management/fetch/cookie_list.html'
    context_object_name = 'cookies'

    def test_func(self, user):
        return user.is_staff

