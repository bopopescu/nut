from flask import Flask
from flask import Response, request

from top import api

app = Flask(__name__)
app.config.from_pyfile('../config/default.py')


@app.route('/recommend', methods=['GET'])
def recommend():
    assert request.path == '/recommend'
    assert request.method == "GET"

    print dir(request)
    # print request.form['keyword']
    # print dir(app.config)
    # print Request.query_string
    return Response("OK")


if __name__ == '__main__':
    # print app.config.get('APP_KEY')
    app.run()
