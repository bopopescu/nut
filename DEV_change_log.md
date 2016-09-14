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