# -*- coding: utf-8 -*-

from flask import Flask
# from top import api
import top.api
import top
import json


app = Flask(__name__)
app.config.from_pyfile('../config/default.py')


def handel(keyword, **kwargs):
    app_key = app.config.get('APP_KEY')
    app_secret = app.config.get('APP_SECRET')

    req = top.api.AlibabaOrpRecommendRequest()
    req.set_app_info(top.appinfo(app_key, app_secret))
    req.appid=2750
    req.call_source="TOP_GUOKU"

    istk = kwargs.pop('istk', True)
    ismall = kwargs.pop('ismall', False)
    count = kwargs.pop('count', 20)

    params = dict()

    params.update(
        {
            "istk":     str(istk),
            "mall":     str(ismall),
            "count":    count,
        }
    )

    if keyword:
        params.update({
            'keyword':keyword,
        })
    app.logger.info(params)
    req.params = json.dumps( params )

    try:
        resp= req.getResponse()
        res = resp['alibaba_orp_recommend_response']['recommend']
        return json.loads(res)
    except Exception, e:
        app.logger.error(e.message)
        return None

