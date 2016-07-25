# -*- coding: utf-8 -*-
from __future__ import absolute_import
from flask import Flask
from flask_restful import Api


app = Flask(__name__)
res_api = Api(app)
app.config.from_pyfile('../config/default.py')


from applications.models.base import db
from applications.api.keywords import SearchHistoryView, UserSearchHistoryView



res_api.add_resource(SearchHistoryView, '/keywords/')
res_api.add_resource(UserSearchHistoryView, '/keywords/<user_id>/')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")