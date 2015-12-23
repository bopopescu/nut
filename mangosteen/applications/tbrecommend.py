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

    istk = kwargs.pop('istk')

    params = {
        "keyword": keyword,
        "istk": True,
        "mall": False,
        "count":    "20",
    }

    # req.params={"keyword":"nike",      "istk":"true",      "count":"20" }
    req.params = params

    try:
        resp= req.getResponse()
        # print(resp)
        res = resp['alibaba_orp_recommend_response']['recommend']
        return json.loads(res)
    except Exception, e:
        print(e)

