5. the great performance leap is to add backface-visibility: hidden; to fix elements !

4. dig functions for article

3. selection entity page js rebuild --- not finished 

2. user change email mail 认证 --- not finished
1. new register user mail 认证 --- not finished

0 . to use assignment_tag replace global context processors

to know WHAT is css trigger ? 

to  remove unpublished article in article tag page !!  -- DONE. 

to  make google analysis js async --- already async , the article is written 2009 
http://www.stevesouders.com/blog/2009/12/01/google-analytics-goes-async/

to test event read function working 
   

to test incr decr functions
    1. incr a value that is empty 
    2. incr a value that has value 
    3. decr a value 0 
    4. decr a value greater than 0 


to implement article tag
    1. in selection article list view , add article tags context
    2. in selection article list item template add tag 
    3. in article  detail page add tag item 
    4. share css 

to implement article dig: 
    1. add dig model 
    2. add  ulr for dig action
    3. add view for article dig 
    4. front end dig in article list 
    5. front end dig in article detail 
    
===== 2015 - 10 -22 == START =====

5. minor css adjusts

4. hide footer elements in xs screen

3. management selection articles list , add search 

2. entity detail page : add related article block

1. management entity management 
   a. add selection entity tab 
   b. add search for brand and entity title 
    
======== 2015 - 10 -18  start ===========
========= 2015 - 10 -18 submmmit to master ========


1. 精选商品页中的待发布和已下架完全区分开；
2. 爬虫在爬到已下架的精选商品的时候，会把状态从商品更改为冻结。
 
=== 2015-10-15 ================================


6. add Event-related-article management 
   
   CREATE TABLE `core_event_related_articles` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `event_id` integer NOT NULL,
    `article_id` integer NOT NULL,
    UNIQUE (`event_id`, `article_id`)
    );
    ALTER TABLE `core_event_related_articles` ADD CONSTRAINT `article_id_refs_id_71111e46` FOREIGN KEY (`article_id`) REFERENCES `core_article` (`id`);
    ALTER TABLE `core_event_related_articles` ADD CONSTRAINT `event_id_refs_id_9a1e89d0` FOREIGN KEY (`event_id`) REFERENCES `core_event` (`id`);

5. add article search , order by score 
4. change site.js , use /tag/name/  for tag entity page link
3. tag_entities_url url pattern capture change to (\w+) , to capture hash.
2. user index page - sidebar, user tag page , tag link updated to hash form. 
1. remove ga/ jiathis form article detail page, in m.guoku.com domains

=== 2015 - 10 - 12 === start =================


==== 2015-10-12  =========== MERGED TO  MASTER 
8. view optimize : use selected_related , prefetch_related to reduce sql hits.

7. block ISP ad injection

6. 更新 ariticle api , html_unescape article content , before sent to client 

5. 保存文章的时候提取相关商品列表保存

4. Article model 加入related_entities m2m 字段 (需要执行 SQL 语句)
   CREATE TABLE `core_article_related_entities` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `article_id` integer NOT NULL,
    `entity_id` integer NOT NULL,
    UNIQUE (`article_id`, `entity_id`)
    );
    ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `entity_id_refs_id_8f4ed529` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
    ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `article_id_refs_id_c5544a89` FOREIGN KEY (`article_id`) REFERENCES `core_article` (`id`);
    
    详情见 ： 日常开发文档／图文／文章 related entity.MD
    

3. 新增前台，标签 文章列表页
2. 文章列表页顶部加入置顶标签显示
1. 后台标签管理增加 置顶文章标签功能 
    
    (需要手动执行 SQL 语句)
    
    详情见 ： 日常开发文章／tag／实现 文章 tag 置顶 功能.MD

    ALTER TABLE `core`.`tag_tags` 
    ADD COLUMN `isTopArticleTag` TINYINT(1) NOT NULL DEFAULT 0 AFTER `image`;
   
    
=== 2015-10-10 =====  start ===========================