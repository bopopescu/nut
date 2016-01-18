
1. show baichuan recommend

=================================
=================================
### merged to master 2016 － 1 － 18
=================================
=================================

5. use CBV for user list 
4. user list search
3. baichuan recommendation  (hide for now)
2. user set to author 
1. a bookmark for youzhan's taobao product adding , not for web 
   but put in doc anyway

##action  

need syncdb 


2016-1-13 start 

=================================
=================================
### merged to master 2016 － 1 － 12
=================================
=================================

6. add home link in store2015 page 
5. store2015 entity list display bug fix
4. freeze entity liker won't display bug fix
3. in guoku editor 
   a. if article's change is not saved , user can not leave page without passthrough a confirmation dialog;
   b. removeFormat button now working ok 
   c. after past html , the style in other content won't be removed
  
2. fix register page word error (Have an Account? )
1. fix user can not send verify mail , if user location is not in default list (app reged user)

###action 
### 翻译有更新
  需要  compilemessages
  需要重新启动 让翻译生效 

=================================
=================================
### merged to master 2016 － 1 － 8
=================================
=================================

3. fast click optimize for mobile browsers 
2. m.guoku.com store2015 page , weixin browser , entity click to app download 
1. fix store 2015 weibo share page pic bug

2016－1-8 start

=================================
=================================
### merged to master 2016 － 1 － 7
=================================
=================================

5. guoku assigned email , no verify , alert to change mail . 
4. store 2015 front
3. 搜索记录同时记录用户的ip和agent
2. 首页瀑布流
1. update redis key user_last_verify_time_id to user_last_verify_time:id

### 翻译有更新
  需要  compilemessages
  需要重新启动 让翻译生效 

### action

    ALTER TABLE `core`.`core_search_history` 
    ADD COLUMN `ip` VARCHAR(45) NULL COMMENT '' AFTER `search_time`,
    ADD COLUMN `agent` VARCHAR(255) NULL COMMENT '' AFTER `ip`;
    
    ALTER TABLE `core`.`core_search_history` 
    CHANGE COLUMN `key_words` `key_words` VARCHAR(255) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL COMMENT '' ;

    
1 ： 果库Top 100 淘宝卖家    
    
2015-12-30
===
    
---    
=================================
=================================
### merged to master 2015-12-28
=================================
=================================



4.  no more christmas logo
3.  fix management search paging bug
2.  seller web page 
1.  seller management update

=================================
=================================
### merged to master 2015-12-23
=================================
=================================

7. user page side bar (not user index page side bar) , 
    disable user article link if user do not have article (done)
     
6. user page, display user article when user has article 
    (currently only display when user can write) (done)
    
5. xs screen selection_entity page bg-color : #f8f8f8 （done）
4. display 2 entity in a row (done)
3. display all note on selection entity page.(done)


------  not finished  ---- 
2. friendly link , new style (NOT finished )
1. in wechat browser , if product is from taobao/tmall , 
    buy button jump to app download page (NOT finished)
----------------


1. add seller section management views and templates



### Action
1.  drop table : seller_seller_profile
2.  drop table : seller_seller_profile_related_articles   
3.  need Sync DB 


2015-12-20 

=================================
=================================
### merged to master 2015-12-17
=================================
=================================

2. fix event page selection entity css broken bug 
1. fix liker list page css broken bug 
  
#### Action
  * update django-sendcloud: 

        sudo pip install git+git://github.com/guoku/django-sendcloud@master
          
        
  * update db: 

        CREATE TABLE `core_sd_address_list` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `address` varchar(45) NOT NULL,
        `name` varchar(45) NOT NULL,
        `description` varchar(45) NOT NULL,
        `created` datetime NOT NULL,
        `members_count` integer NOT NULL
        );

INSERT INTO `core`.`core_sd_address_list` (`address`, `name`, `description`, `members_count`, `created`) VALUES ('gk_users_1@maillist.sendcloud.org', 'gk_users_1', 'gk_users_1', '11017', '2015-12-16 17:04:21');

####Changelog:

1. fix feed read counter bug


2. 首页瀑布流
1. update redis key user_last_verify_time_id to user_last_verify_time:id

-------

fix bug: category entities order by olike can't load more entity when screen scroll to bottom.

-------

1. 用户注册、激活、需改信息..时，对SendCloud的操作改为使用celery;
2. 动态获取和创建SendCloud地址列表;
3. 只有激活了的邮箱才会加入到sendcloud地址列表；
4. 开始着手写test，写了一些关于account和edm的。

-------

4.  minor bug fix 
3.  user liker app in entity detail page
3. event page, m.guoku.com, simple title (not finish)
2. add seller management files
1. add seller model 

### Action  
need syncdb  
for new seller table




=================================
=================================
### merged to master 2015-12-10
=================================
=================================


4.  minor display bug fix 
3.  user liker app in entity detail page / restful API 
2.  add analysis.guoku.com's tracking code 
1.  make sure this is no overflow in counter values.


### ACTION
ALTER TABLE `core`.`core_article` 
CHANGE COLUMN `read_count` `read_count` INT(32) UNSIGNED ZEROFILL NULL DEFAULT 0 ,
CHANGE COLUMN `feed_read_count` `feed_read_count` INT(32) UNSIGNED ZEROFILL NULL DEFAULT 0 ;





=================================
=================================
## merged to master 2015 - 12 - 3
=================================
=================================

5.修改edm收件地址列表，从测试列表改为正式列表。修改settings所以需要重启服务
4. article page weixin share url move to m.guoku.com 
3. user email verify functions 
2. user setting pages css refactor  
1. add some tests for tag(It's not enough). by judy 
 
==== 2015-12-03 ==== start 


## merged to master 2015 - 11 -30

5. FIX tag list page  paging function bug
4. event list page is now the default event link target
3. user likes page category filter 
2. user following/fans page refactor , add followee/follower recent likes 
1. user index page minor fix 
0. a office test server setting/deploying files 

==== start 2015-11-28 ====

## merged to master 2015-11-27

5. fix broken links on tag/hash-code
4. fix user tag list dup bug
3. fix user page follow/unfollow action bug 
2. event list page require js management 
1. event page require js management 
=== 2015 - 11 - 26 ======

1.修复django-sendcloud不能直接从setting读取配置的问题
2.补全丢失的settings信息
3.创建专题的时候隐藏top_tag，默认值为''
4.修改专题时隐藏top_tag
5.修改edm预览页面中静态图片地址

===== 2015 - 11 - 25 =======


2. event page add new recommendation section 
##Action remote/local db : need run sql  
        ALTER TABLE `core`.`core_show_editor_recommendation` 
        ADD COLUMN `section` VARCHAR(64) NOT NULL DEFAULT 'entity' AFTER `created_time`;

1. event page display update 

##Action local :merge master to dev -> launch pad functions 
##Action local :  ./manage.py syncdb --settings=......
   

=== 2015 11 24 ===

3. article_feed_read_counter deploy to 48 , cron tab 
2. fix API user like  500 error when user has no likes
1. entity detail page bug fix  , (a @property is lost when merge with judy's commit )

====== start 2015-11-23 ====

### merged to master  2015-11-23

1. 把用户页（喜爱，点评，文章，标签）加入requireJS
2. 搜索结果页加入requireJS

===== 2015 - 11 - 24 =======


3. m.guoku.com article page , wechat access , all link direct to http://www.guoku.com/download/
2. need deploy article_feed_counter_save.py to crontab
1. feed read count , need run sql  ,( already excuted on 10.0.2.90 core )

##ACTION : run sql , ( already run on 10.0.2.90   core )

ALTER TABLE `core`.`core_article` 
CHANGE COLUMN `read_count` `read_count` INT(10) UNSIGNED ZEROFILL NULL DEFAULT 0 ,
ADD COLUMN `feed_read_count` INT(10) UNSIGNED ZEROFILL NULL DEFAULT 0 AFTER `read_count`;


##ACTION : need run on production server FOR  sendCloud  : 

sudo pip install git+git://github.com/guoku/django-sendcloud@master

=== 2015 - 11 - 21 ====
1. 把记录搜索的方法record_search改成了用delay调用。


TODO : 现在移动端的标签还都是个人标签，是否需要改成全局标签

====  2015 - 11 -18 =====
2. new front-end for entity-detail page
1. add placeholder bug  quick fix for register page on IE8 

==== 2015 - 11  - 17  =====
0. 给module Search_History的record方法加了一点注释。
1. 把tag/articles下的页面加入RequireJS
2. 把category下的页面加入RequireJS，并作为滚动到页底自动加载
3. 在model research_history里的记录搜索函数，判断用户是否为游客的时候，换为一种更加安全的方式

1. 合并EDM到dev
2. 调整EDM内容样式
3. SD地址列表成员更新信息不能用update接口，需要先delete再add
4. EDM上线前需要先更新线上环境的django-sendcloud

************* start 2015-11-13 *************************

### merged to master 2015-11-12 

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

### 2015-11-02 ===  merged to master =============================


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

### 2015 - 10 -18 submmmit to master ========


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


### 2015-10-12   MERGED TO  MASTER 
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