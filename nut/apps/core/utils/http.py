#encoding=utf8

from django.http import HttpResponse
# from django.utils import simplejson as json
import json

class JSONResponse(HttpResponse):
    def __init__(self, data, status=200, content_type='application/json; charset=utf8'):
        _content = json.dumps(data, indent=2)
        super(JSONResponse, self).__init__(
            content = _content,
            content_type = content_type,
            status = status
        )


class SuccessJsonResponse(JSONResponse):

    def __init__(self, data = None):
        super(SuccessJsonResponse, self).__init__(data, 200)


class ErrorJsonResponse(JSONResponse):
    def __init__(self, status, data = None):
        super(ErrorJsonResponse, self).__init__(data, status)


__author__ = 'edison'
