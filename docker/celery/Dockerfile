FROM        ubuntu:14.04
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN         apt-get clean
RUN         apt-get update --fix-missing && apt-get -y install python2.7 \
                    python2.7-dev python-pip gcc make supervisor libmysqlclient-dev git libmagickwand-dev
COPY        requirements.txt /tmp/requirements.txt
RUN         pip install -r /tmp/requirements.txt
COPY        supervisord.conf /etc/supervisor/conf.d/supervisord.conf
VOLUME		["/data/www/nut", "/tmp/"]
WORKDIR     /data/www/nut
#EXPOSE 		8000
CMD         ["/usr/bin/supervisord"]