======================================

Order.alipay_qrcode_frame_page_url

这是一个果库页面的 url
这个页面里 只有一个 当前订单 的 支付宝支付 二维码

IOS 可以用这个页面进行订单支付。 



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