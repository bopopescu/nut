1.  implement alipay rsa crypto methods 

action 
    1. need install m2crypto 
        pip install M2Crypto
    
    
=====================
merged to master 8/31
====================
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