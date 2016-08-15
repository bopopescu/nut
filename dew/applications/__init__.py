# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from flask_restful import Api

app = Flask(__name__, static_url_path='/static')
res_api = Api(app)
app.config.from_pyfile('../config/default.py')


from applications.api.keywords import SearchHistoryView, UserSearchHistoryView

# TODO: set record key word URI
res_api.add_resource(SearchHistoryView, '/keywords/')
res_api.add_resource(UserSearchHistoryView, '/keywords/<user_id>/')


from applications.web.views.hotwords import HotWordsView

app.add_url_rule('/hotword/', view_func=HotWordsView.as_view('hot_words'))
# app.add_url_rule('/hotword/add/', )


from applications.api.article import ArticleTextRank

res_api.add_resource(ArticleTextRank, '/article/<article_id>')


from applications.models.base import db
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")