# -*- coding: utf-8 -*-
from __future__ import absolute_import
from flask import Flask
from flask_restful import Api


app = Flask(__name__)
res_api = Api(app)
app.config.from_pyfile('../config/default.py')



from applications.api.keywords import SearchHistoryView



res_api.add_resource(SearchHistoryView, '/keywords/')


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")