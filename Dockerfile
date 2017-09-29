FROM python:2.7

COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y \
        gcc \
        gettext \
        mysql-client libmysqlclient-dev \
        postgresql-client libpq-dev \
        sqlite3 libmagickwand-dev \
   --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ARG PIP_INDEX_URL=https://pypi.python.org/simple
ENV PIP_INDEX_URL ${PIP_INDEX_URL}

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY nut /usr/src/app

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
