Change Log
==========

### Ver 2.2.2


1. **core_buy_link** 表增加 **status** 字段。
2. **core_buy_link** 表增加 **shop_link** 字段。
3. **core_buy_link** 表增加 **seller** 字段。
4. 优化 **nickname** 的显示 


### 注：

```
ALTER TABLE core_buy_link ADD COLUMN `status` integer UNSIGNED NOT NULL;
alter table core_buy_link add column `shop_link` varchar(255);
alter table core_buy_link add column `seller` varchar(255);
```



