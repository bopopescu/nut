1.  IOS, Android 4.1 版本会用嵌入浏览器打开图文详情页
2.  访问的request 均以 m.guoku.com 为host
3.  后台判断，m.guoku.com 请求的页面， 会在 body tag 的 class 中加入 mobile-body
4.  css 会定义 ,
        显示： mobile ONLY 的元素 
              .for-mobile 
        隐藏： browser ONLY 的元素
              .for-browser
5. 有些JS 功能是不需要使用的，js 需要设置一个变量 ， is_mobile , 
   前端程序访问这个变量来决定是否 实现某些功能。
6. 文章页 ，商品的链接 ， 会处理成为这样的格式   
             
            guoku://entity/12321321/ 
           
           其中的数字为 商品 id 

           作者的链接,   会处理称为 
           
           guoku://user/2332234/  
                  
           的格式，其中数字为 用户 id  
           
7.  文章页的 “大家都在看” 推荐文章列表， 在 mobile端 会隐藏。
         
         