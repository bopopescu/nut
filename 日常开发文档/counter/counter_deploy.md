部署计数器，和保存阅读数

1. alter table （SQL COMMAND）

ALTER TABLE `core`.`core_article` 
ADD COLUMN `read_count` INT ZEROFILL UNSIGNED NULL AFTER `showcover`;

todo : this column is NOT null , or it can not be indexed !


2.  部署代码

2.5 测试计数器工作正常

3. sudo crontab -e   , 打开的编辑器里加入下面一行,并保存

*/30 * * * * /usr/local/bin/python /data/www/nut/script/counter/article_counter_save.py 
 