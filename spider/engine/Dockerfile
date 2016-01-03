FROM 		ubuntu-upstart:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN			apt-get update && apt-get install -y python-dev python-pip \
                libxml2 libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
RUN         pip install -U Scrapy scrapyd -i http://pypi.douban.com/simple
WORKDIR     /data/www/spider/
EXPOSE      6800
RUN         mkdir /etc/scrapyd/
COPY        scrapyd.conf /etc/scrapyd/scrapyd.conf