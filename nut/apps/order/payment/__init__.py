
import urllib
import time
import hashlib
import json
import top
import itertools
import mimetypes


def sign(secret, parameters):
    #===========================================================================
    # '''签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    #===========================================================================
    # 如果parameters 是字典类的话
    if hasattr(parameters, "items"):
        keys = parameters.keys()
        keys.sort()

        parameters = "%s%s%s" % (secret,
            str().join('%s%s' % (key, parameters[key]) for key in keys),
            secret)
    sign = hashlib.md5(parameters).hexdigest().upper()
    return sign

def mixStr(pstr):
    if(isinstance(pstr, str)):
        return pstr
    elif(isinstance(pstr, unicode)):
        return pstr.encode('utf-8')
    else:
        return str(pstr)

class appinfo(object):
    def __init__(self,appkey,secret):
        self.appkey = appkey
        self.secret = secret

def getDefaultAppInfo():
    pass


def setDefaultAppInfo(appkey,secret):
    default = appinfo(appkey,secret)
    global getDefaultAppInfo
    getDefaultAppInfo = lambda: default


