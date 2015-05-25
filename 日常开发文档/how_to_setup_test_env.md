1. install mysql 
2. create a database named "core"
3. in dev machine , modify django setting file , 
   point database to it.
4. run  ./manage.py syncdb --settings='settings.dev_anchen'
   for db init 
5.  install redis
6.  install celery 


/opt/mysql5/bin/mysqldump --single-transaction --flush-logs -u root  core > core.sql
/opt/mysql5/bin/mysqladmin -uroot stop-slave
/opt/mysql5/bin/mysqladmin -uroot start-slave
