FROM        ubuntu:14.04
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN         apt-get clean
RUN         apt-get update && apt-get -y install python2.7 \
                    python2.7-dev python-pip gcc make libffi-dev supervisor libmysqlclient-dev
RUN         pip install -U flask requests gunicorn gevent flask-cli MySQL-python \
                    Flask-JSON Flask-SQLAlchemy flask-restful flask-marshmallow marshmallow-sqlalchemy
COPY        supervisord.conf /etc/supervisor/conf.d/supervisord.conf
VOLUME		["/data/www/dew", "/tmp/"]
WORKDIR     /data/www/dew
EXPOSE 		8000
CMD         ["/usr/bin/supervisord"]