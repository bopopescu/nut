Change Log
==========
### Ver 4.3.4
1. 分类增加拼音排序
2. 商品搜索 title 增加拼音查找

```
pip install xpinyin
```
```
alter table core_sub_category add column `alias` varchar(128) NOT NULL AFTER `title`;
```

### Ver 4.3.3
1. 购买链接增加防盗链
2. 精选页面 UI 更新
3. 修复添加商品却是店铺信息 bug
4. 后台管理 UI 升级


### 注:
```
ALTER TABLE `core`.`core_buy_link` ADD COLUMN `foreign_price` DECIMAL(20,2) NULL COMMENT '' AFTER `seller`;
```



### Ver 4.3.2
1. 更新用户个人页 ui
2. 商品单页 购买链接 改为服务器跳转。（除淘宝）
3. webUI 更新（专题页）
4. 专题BANNER 增加了辅助字段。

ALTER TABLE `core`.`core_event_banner` 
ADD COLUMN `background_image` VARCHAR(255) NULL DEFAULT NULL AFTER `updated_time`,
ADD COLUMN `background_color` VARCHAR(14) NULL DEFAULT 'fff' AFTER `background_image`;


### Ver 4.3.1
1. v4 增加 discover 
2. solr 替换 sphinx 搜索引擎
3. 增加店铺链接
4. 优化搜索结果

```
ALTER TABLE `core`.`core_buy_link` ADD COLUMN `foreign_price` DECIMAL(20,2) NULL COMMENT '' AFTER `seller`;
```


### Ver 4.3
1. 后台图文编辑增加标签 
2. 修正添加商品 bug
3. category 增加封面图片
4. 更新 404， 500 页面

```
alter table core_category add column `cover` varchar(255) NOT NULL;
```

### Ver 4.2.9
1. 重构标签
2. 页面 title 关键词调整

### Ver 4.2.8
1. 支持 emoj
2. 后台支持 buy link 检索
3. 分类页，去除以下架的商品
4. 图文上线

### Ver 4.2.7（2015-07-06）
1. 增加商品发布到 U站
2. 增加 django-debug-toolbar 
3. 增加 商品喜爱计数器缓存
4. 支持 果库内嵌浏览器 去除导航栏， 测试用 safari ， 改了 user agent  string , 加 orange 进去， 访问 http://test.guoku.com/articles/9/ ， 应该不出现导航栏。  

### Ver 4.2.6（2015-07-02）
1. 完善推荐算法， 去除部分下架商品。
2. 上传 png 自动转换成 jpeg

### Ver 4.2.5 （2015-07-01）
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

### Ver 4.2.4
1. 增加 Article (图文) Sitemap
2. 增加 Article (图文) Rss
3. bug fixes


### Ver 4.2.3 （2015-06-24）


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



