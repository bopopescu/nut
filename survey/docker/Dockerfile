FROM        ubuntu:14.04
MAINTAINER	jiaxin	<jiaxin@guoku.com>
#COPY		sources.list.trusty /etc/apt/sources.list
COPY        requirements.txt /tmp/requirements.txt
RUN         apt-get update && apt-get -y install python2.7 python2.7-dev python-pip supervisor libmysqlclient-dev
RUN         pip install -r /tmp/requirements.txt
COPY		gunicorn /etc/default/gunicorn
COPY        supervisord.conf /etc/supervisor/conf.d/supervisord.conf
WORKDIR     /data/www/survey
EXPOSE 		8000
CMD         ["/usr/bin/supervisord"]