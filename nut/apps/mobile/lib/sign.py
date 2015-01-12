from hashlib import md5
from apps.core.utils.http import ErrorJsonResponse
# from http import ErrorJsonResponse
# from mobile.models import Apps


class MissParamError(Exception):
    pass


class ApiKeyError(Exception):
    def __init__(self, key):
        self.key = key
        self.message = "Invalid Api Key %s" % key

    def __str__(self):
        return repr(self.message)


class SignError(Exception):
    def __init__(self, sign):
        self.sign = sign
        self.message = "Invalid client sign %s" % self.sign
    def __str__(self):
        return repr(self.message)


def _check_request_param(param):
    if 'api_key' not in param.keys() and 'sign' not in param.keys():
        raise MissParamError(u'need api_key and sign')


def _check_sign_md5(param):
    try:
        app_object = Apps.objects.get(api_key = param['api_key'])
    except Apps.DoesNotExist:
        raise ApiKeyError(param['api_key'])
    _client_sign = param['sign']

    sort_key = sorted(param)
    if 'avatar_data' in sort_key:
        sort_key.remove('avatar_data')
    sort_key.remove('sign')
    sum = ''
    for key in sort_key:
        sum += '%s=%s' % (key, param[key])
    _sign_raw = sum + app_object.api_secret
    _server_sign =  md5(_sign_raw.encode('utf-8')).hexdigest()
    if _client_sign == _server_sign:
        return True
    else:
        raise SignError(_client_sign)

def check_sign(func):
    def check_sign_wrapped(request, *args, **kwargs):
        _param = request.REQUEST.copy()
        _req_uri = request.get_full_path()
        try :
            _check_request_param(param=_param)
            _check_sign_md5(_param)
        except MissParamError, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'miss_param',
                    'message' : e.message,
                },
                status = 400
            )
        except ApiKeyError, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'api_key',
                    'message' : e.message,
                },
                status = 400
            )
        except SignError, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'sign',
                    'message' : e.message,
                },
                status = 400
            )

        return func(request, *args, **kwargs)

    return check_sign_wrapped


__author__ = 'edison'