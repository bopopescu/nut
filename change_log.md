Change Log
==========
### Ver 2.2.5
1. spider update 可以检查 淘宝商品价格。 

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



