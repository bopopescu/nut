Change Log
==========
### Ver 2.2.5
1. spider update 可以检查 淘宝商品价格。 
2. 增加 amazon 图书入库。
3. 部署计数器，和保存阅读数

```
alter table （SQL COMMAND）
ALTER TABLE `core`.`core_article` 
ADD COLUMN `read_count` INT ZEROFILL UNSIGNED NULL AFTER `showcover`;
```

2.  部署代码

2.5 测试计数器工作正常

3. sudo crontab -e   , 打开的编辑器里加入下面一行,并保存

*/30 * * * * /usr/local/bin/python /data/www/nut/script/counter/article_counter_save.py 

### Ver 2.2.4
1. 增加 Article (图文) Sitemap
2. 增加 Article (图文) Rss
3. bug fixes


### Ver 2.2.3 （2015-06-24）


1. **core_buy_link** 表增加 **status** 字段。
2. **core_buy_link** 表增加 **shop_link** 字段。
3. **core_buy_link** 表增加 **seller** 字段。
4. 优化 **nickname** 的显示 
5. 增加微信登陆


### 注：

```
ALTER TABLE core_buy_link ADD COLUMN `status` integer UNSIGNED NOT NULL;
alter table core_buy_link add column `shop_link` varchar(255);
alter table core_buy_link add column `seller` varchar(255);
```



