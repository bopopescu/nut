docker run -t -i -d -v /data/www/nut/:/data/www/nut/ -v /data/var/logs/django/:/tmp/ -p 10.0.2.47:8000:8000 nut
docker run -d  -t -i -v /data/www/nut/:/data/www/nut/ -v /data/var/logs/celery/:/tmp/ celery
