
1. 给module Search_History的record方法加了一点注释。

===== 2015 - 11 - 12 =======


1. 把tag/articles下的页面加热RequireJS
2. 把category下的页面加入RequireJS，并作为滚动到页底自动加载
3. 在model research_history里的记录搜索函数，判断用户是否为游客的时候，换为一种更加安全的方式

===== 2015 - 11 - 12 =======


2. remove 1111 gif on header 
1. article page dig
   
===== 2015 - 11 - 12 =======


	need run SQL  : 

	CREATE TABLE `core_search_history` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer,
    `key_words` varchar(255) NOT NULL,
    `search_time` datetime
	);
	ALTER TABLE `core_search_history` ADD CONSTRAINT 	`user_id_refs_id_371b5c0a` FOREIGN KEY (`user_id`) REFERENCES 	`core_gkuser` (`id`);

· 每次用户搜索的时候，都通过celery把搜索时间、关键字、用户记录下。

=== 2015-11-09 ================================


1. 修改了gruntfile.js，会自动把web/app下说有名称为*_app.js的文件build到web/jsbuild下，build后的名称为*_app_build.js；
2. 修复了message页，屏幕不断向下滚动时，会不断给页面增加空白块的bug；
3. 把discovery 页的js模块使用RequireJS加载。

=== 2015-11-6============================ 

3. article list page new front end 
2. add hidden img for app share , element id = 'share_img'
1. remove header render for article page 

关于客户端分享文章，图片问题

1. 客户端抓取页面（m.guoku.com/articles/id/）的第一张图片。
   现在第一张图片是双十一促销gif（in header）（新版 DEV 已经移除）

2. quick FIX 
   m.guoku.com 取消渲染 header 
   
3. more. 以后的 ios 版本可以用下面的方式拿到 图文 分享图片
   在图文详情页，有加入一个隐藏 div , ID="share_img"
   div 中有 img 元素作为文章分享图片。
   
   IOS NEED fix ：
4. 文章分享中 文章的地址， 应该是www.guoku.com的地址，而不是 m.guoku.com 的地址。
   
 

====== 2015 - 11 -5 ============


1. Event Top entity functions

    need run SQL  : 
    
    ALTER TABLE `core`.`core_event` 
    ADD COLUMN `toptag` VARCHAR(30) NOT NULL AFTER `created_datetime`;

=== 2015-11-4============================ 


1. event template adjust for 1111 event 

==== 2015-11-3 ===



给创建商品页添加了chosen插件。

=== 2015-11-02 ===  merged to master =============================


6. IE8 compatible fix  -- done 
5. need fix scroll top header hidden bug  -- done 
4. top menu auto show/hide on scroll -- done
3. event page read red dot indicator -- done
2. sns bind page red dot indicator -- done
1. entity selection page autoload , paging --- done

note: the great performance leap(scroll frame rate) is to add backface-visibility: hidden; to fix elements.
==================== new frontend ==========
============= document in "前端JS开发" =======

5. 添加select插件chosen到后台的商品页。
    
4. dig functions for article (server side/Front End not implemented)

   *****  need syncdb *******, 
   new model :  Article_Dig

2. selection entity page js rebuild --- see ( new frontend )
1. to use assignment_tag on footer's friendly link
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