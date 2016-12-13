1. add is2016store and is2015store to Seller_Profile

ALTER TABLE `core`.`seller_seller_profile` 
ADD COLUMN `is2016store` TINYINT(1) NOT NULL DEFAULT 1 AFTER `related_article_id`;

ALTER TABLE `core`.`seller_seller_profile` 
ADD COLUMN `is2015store` TINYINT(1) NOT NULL DEFAULT 1 AFTER `is2016store`;


=========================

2. remove da yue cheng pop up 
1. try to fix counter bug (m.guoku.com article page , post couter fail )

=============================
3. fix make article slug bug
2. change topad article link
1. fix article counter bug 

====================================
====================================

4. h5 for da yue cheng  -- lq
3. top bar for web  -- lq
2. login redirect to index 
1. download csv order data 

action 
    pip install unicodecsv
    
    unicodecsv already added to requirements

=========================
==========================

1.  article slug 
      a . add article_slug field to Article model 
      b . generate slug for current articles 
      c . for new article,  update Article's save method , generate article_slug on the run 
      d . update crawler method, 
        
ALTER TABLE `core`.`core_article` 
ADD COLUMN `article_slug` VARCHAR(128) NULL AFTER `origin_url`,
ADD UNIQUE INDEX `article_slug_UNIQUE` (`article_slug` ASC);

    add generate_article_slug.py to script/Article_related dir
    
    deploy : 
     a. on production db , run 
        ALTER TABLE `core`.`core_article` 
        ADD COLUMN `article_slug` VARCHAR(128) NULL AFTER `origin_url`,
        ADD UNIQUE INDEX `article_slug_UNIQUE` (`article_slug` ASC);
        
        
     b. on 10.0.2.48 :
        python /data/www/nut/script/Article_related/generate_article_slug.py
        
        5 min runtime most 
        
        
        

        

========================
merged to master 11-11
========================

5. about page update  -- lq 
4. offline shop update -- lq 
3. cart item rule for discount skus 


    a. there will be special sku for discount
    b. scan those sku will let system try to add special sku to the cart
    c. before the insert sku to the cart ,a rule set will be checked.    
    d. if the rule can not apply to the current cart item combination
        the sku_add_exception will be raised 
    e. when user checkout , the coupon rule will be checked again
        if rule is failed , will raise CartException 
        
2. article slug url 
1. add api for restframework token auth -- not finished 
    
action: 
    -------  install  django-uuslug lib
    
    pip install django-uuslug 
    
    on test machin (48) : 
    
    export LC_ALL="en_US.UTF-8"
    export LC_CTYPE="en_US.UTF-8"
    sudo dpkg-reconfigure locales
    sudo pip install django-uuslug 
    
    
===================================
merged to master 11/1 
=====================================


10. update offline shop 
9. event mini logo
8. web new top bar 

7. offline shop management (list, edit)
6. record margin in orderitem 
5. display margin on order list page (seller and checkout )
4. quick edit margin on entity list page 
3. add new sku field for margin 

2. add new user guokumk@guoku.com FOR main seller for dayuecheng event 
   remove fugu@guoku.com 's users ability to change entity creator 
   add guokumk@guoku.com 's user's ability to change entity creator  
    
1. add static data for offline shop 



action : 

ALTER TABLE `core`.`order_sku` 
ADD COLUMN `margin` FLOAT NOT NULL DEFAULT 0 AFTER `discount`;

ALTER TABLE `core`.`order_orderitem` 
ADD COLUMN `margin` FLOAT NOT NULL DEFAULT 0 AFTER `attrs`;


===================================
merged to master 10/26 
=====================================

6. add position field to offline_shop_info

5. 
    move baidu static code to header, 
    remove guoku analytic code
    
4. fix top_ad bug  

3.1 add mobile_url property to Offline_Shop_Info model
 
3. add Offline_Shop view 

2. move GKUser.offline_shops method to Offline_Shop_Info manager

1. add status field to Offline_Shop_Info 

action : 
ALTER TABLE `core`.`offline_shop_offline_shop_info` 
ADD COLUMN `status` TINYINT(1) NOT NULL DEFAULT 0 AFTER `shop_mobile`;

ALTER TABLE `core`.`offline_shop_offline_shop_info` 
ADD COLUMN `position` INT(32) NOT NULL DEFAULT 0 AFTER `status`;

Offline_Shop_Info.objects.active_offline_shops() 
TO GET ALL ACTIVE  Offline_Shop_Info instances 
 
Offline_Shop_Info.mobile_url To get url of mobile page 


===========================

3.  management offline shop list 
2.  new user group (offline shop)
1.  article comment management 

action : need syncdb 
        add Offline_Shop_Info model 
        

to get all Offline_Shop: GKUser.objects.offline_shops()




========================

1.fix sub category empty cause 500 bug

=======================

1.  update shop list h5

=======================
merged to master 10-1
=======================

2. guoku off line shop h5 
1. top_ad management 

 add TopAdBanner table

action : 
    syncdb 
    
    
    

==================
merged to master  9-29 
==================

2. web bug fix  
1. top_ad update  

================

2. seller entity list paging bug fix 
1. top_ad update ,  

=======================

5. detail buylink fix fro seller added entity (manual)
4. about page - lq 
3. fugu h5  - lq 
2. qr_code print - lq
1. top_ad by lq 

==============================================

5. order expire check script (script/order/expire_check.py)
4. order status , default value is waiting for payment 
3. checkdesk order detail page. 

2. sku default attr handle . 
1. special seller, (fugu@guoku.com) , in seller management , can change entity creator

action : 

部署 crontab 脚本, 
位置 nut/script/order/expire_check.py
半小时一次


==========================================
merged to master 9/18 



3.  fix web bug -- lq 
2.  add payment method selection in checkdesk 
1.  order statistics in checkout ui

=================================================

6.  category page, popular page , update -lq
5.  seller order list update , add payment info 
4.  check desk payment , add payment source , and payment note update
3.  fix qrcode print -- lq
2.  add payment_note field
1.  add PaymentLog source 

action : 
ALTER TABLE `core`.`payment_paymentlog` 
ADD COLUMN `payment_note` VARCHAR(128) NULL AFTER `updated_datetime`;


==============================

6.  sku remove PROTECT for OrderItem 
5.  order number remove under dash 

4.  order add a property 'realtime_status', is a wrapper arount order.status
    to handle expired order 
    
3.  seller entity add entity update
   
2.  seller entity list update
    1. sku save will change entity update time 
    2. entity sku order by sku stock
    
1.  seller management list bug fix 
=====================
merged to master 9/8
=====================

a.  only show sku , status= enable 
b. 

======================================
关于 SKU 和 OrderItem , CartItem 的约束


1. OrderItem 的 sku 外键如下定义
        sku = models.ForeignKey(SKU, db_index=True, on_delete=PROTECT)
        
    因此当数据库中 , 某个 sku 被 OrderItem 指向后, 当试图删除 该sku时, 
    会抛异常, 阻止 sku 被删除。 后台管理界面表现为删除 sku 不成功(界面未跟进)
    
2. CartItem 的 sku 外键定义如下
        sku = models.ForeignKey(SKU, db_index=True)
    因此,当数据库中, 某个 sku 被 CartItem 指向后, 试图删除 该sku时,
    除了 sku 会被删除, 对应的 cartitem 也会被删除, 
    这是 django 数据库的缺省行为
    
3. 可以把 sku status 设置为 disable 


4. 商品详情页,只显示 enable 的SKU (@jiaxin)

======================================

Order.alipay_qrcode_frame_page_url

这是一个果库页面的 url
这个页面里 只有一个 当前订单 的 支付宝支付 二维码
 
=======================================
1. OrderItem 生成的时候会记录如下字段
    ------------------
    item_title : 商品名
    image : 商品主图
    entity_link : 商品果库链接
    attrs : SKU 的属性值
    ------------------
    同时有如下 property 
    attrs_display : 显示 SKU 的 attr
    
2. 判断订单是否超时
    @property 
    Order.should_expired 
    
3. 当订单超时, 执行 Order.set_paid() 方法会抛出异常

4. 用户checkout 时, 如果某SKU 库存不足, checkout 会失败,并抛出异常。
用户checkout 时, 如果成功创建订单, 会减库存。

5. 新增 Order.set_expire 方法, 该方法会被一个 定时脚本 (间隔一小时) 调用
set_expire 方法会把订单中的库存还原。

========================================


6. other bugs 
5. selection entity and article page css update lq,
4. merge lq's branch  :  lq_refactor_old_pages (web ADD entity  and other js test)

------------

3. Order.set_expired method to set the expire method and update sku stock 
2. Order.should_expired  property , to see if a order should be expired
1. update sku stock after checkout (used to be after payment)

======================================

3.  move checkout method from GKUser into CartItem Manager
2.  fix order_item serialize problem 
1.  add field's to order item 

action : 

ALTER TABLE `core`.`order_orderitem` 
ADD COLUMN `item_title` VARCHAR(256) NULL DEFAULT NULL AFTER `promo_total_price`,
ADD COLUMN `image` VARCHAR(256) NULL DEFAULT NULL AFTER `item_title`,
ADD COLUMN `entity_link` VARCHAR(256) NULL DEFAULT NULL AFTER `image`,
ADD COLUMN `attrs` LONGTEXT NULL DEFAULT NULL AFTER `entity_link`;

<!--action -->
    <!--1. need install m2crypto -->
        <!--pip install M2Crypto-->
        <!--------->
        <!--important !!!-->
        <!--if install M2Crypto fail -->
        <!--because of locale.Error: unsupported locale setting-->
        <!--export LC_ALL="en_US.UTF-8"-->
        <!--export LC_CTYPE="en_US.UTF-8"-->
        
        this is failed in test server 


action : 

ALTER TABLE `core`.`order_orderitem` 
CHANGE COLUMN `item_title` `item_title` VARCHAR(256) CHARACTER SET 'utf8' COLLATE 'utf8_bin' NULL DEFAULT NULL ;

========================

3. web bug fix (
    1.消息下拉列表，点击其他地方，隐藏下拉列表；
    2.好点页，商品title  
    3.商品详情页的用户点评中的标签bug（along fix）
    )
2. move recent like query to slave 
1. add user recent like cache
======================
merged to master 8/30 
======================
6.  add search word 
5.  reduce qrcode complexity in sale page 
4.  hao dian ye ,  seller products 
3.  jd entity crawl bug fix 
2.  refactor martin's code to for appliance to PEP8 
1.  top menu js update -- lq, need intensive test 

====================
merged to master 8/25
====================
8. seller recent entity in web seller page 
7. seller personal page shop entity 
6. jd entity add error fix 
5. web frontend update (index, tag, liker ) -- lq 
4. offline check desk ui
3. SKU, Order ,CartItem, OrderItem inherted from BaseModel
2. move BaseModel to independent file
1. remove SKU, Order, CartItem dependency from core.models