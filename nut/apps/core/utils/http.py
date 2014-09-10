from django.http import HttpResponse
# from django.utils import simplejson as json
import json

class JSONResponse(HttpResponse):
    def __init__(self, data, status):
        _content = json.dumps(data, indent = 2, ensure_ascii = False)
        super(JSONResponse, self).__init__(
            content = _content,
            content_type = 'application/json; charset=utf8',
            status = status
        )


class SuccessJsonResponse(JSONResponse):

    def __init__(self, data = None):
        super(SuccessJsonResponse, self).__init__(data, 200)


class ErrorJsonResponse(JSONResponse):
    def __init__(self, data, status):
        super(ErrorJsonResponse, self).__init__(data, status)


__author__ = 'edison'
