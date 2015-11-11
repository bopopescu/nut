2015-8-24

bug : 
    
    不能用 果库+ 抓取如下 url :
    https://item.taobao.com/item.htm?spm=a219r.lm869.14.16.TayDns&id=520427282130&ns=1&abbucket=17#detail
    
    描述： 
    1.  apps/core/forms/entity.py  line 457 , 不能 self.initial['shop_nick'].decode('utf8')
    2.  这段代码计算 entity hash , 如果改动，
        如果再次加入老商品， 老商品的 HASH 和再次加入的 HASH 不同
        会造成重复商品。

fix : 
    

bug : 
    不能用  果库+ 抓取 如下 url:
    http://www.amazon.com/My-Michelle-Texture-Sleeves-Necklace/dp/B00YEJ2X1M/ref=sr_1_2?s=apparel&ie=UTF8&qid=1440378113&sr=1-2&nodeID=1045470
    Exception Value:	
        invalid literal for float(): 32.99 - $34.99
    Exception Location:	/new_sand/guoku/nut/nut/apps/core/utils/fetch/amazon.py in price, line 64
   
fix : 
    
       