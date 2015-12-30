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
    req.appid=2587
    req.call_source="TOP_BC"

    istk = kwargs.pop('istk', True)
    ismall = kwargs.pop('ismall', False)
    count = kwargs.pop('count', 20)
    itemId = kwargs.pop('itemId', None)
    # print type(ismall)

    # params = {
    #     "keyword": keyword,
    # }
    params = dict()

    params.update(
        {
            "istk":     str(istk),
            "mall":     str(ismall),
            "count":    int(count),
        }
    )

    if keyword:
        params.update({
            'keyword':keyword,
        })

    if itemId:
        params.update({
            'itemid': itemId,
        })

    app.logger.info(params)
    req.params = json.dumps( params )

    try:
        resp= req.getResponse()
        # print(resp)
        res = resp['alibaba_orp_recommend_response']['recommend']
        return json.loads(res)
    except Exception, e:
        app.logger.error(e.message)
        return None

