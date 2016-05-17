FROM        ubuntu
MAINTAINER	jiaxin	<jiaxin@guoku.com>
#COPY		sources.list.trusty /etc/apt/sources.list
RUN         apt-get update && apt-get -y install python2.7 \
                    python2.7-dev python-pip gcc make libffi-dev supervisor libmysqlclient-dev git
COPY        requirements.txt /tmp/requirements.txt
RUN         pip install -r /tmp/requirements.txt
#COPY        supervisord.conf /etc/supervisor/conf.d/supervisord.conf
WORKDIR     /data/www/nut
EXPOSE 		8000
#CMD         ["/usr/bin/supervisord"]