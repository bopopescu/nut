

1.  'H&M'  这样的tag_name ， 无法被原有 URL CONF 解析

   解决方法: urllib.quote 可以 把 & 符号 替换成 “％26” 这样 URL 就可以接受了
             在 VIEW 中 需要把  tag_name  'unquote' 回来，
              参见 TagEntitiesView
                 和  ArticleTagListView 中 的 get 方法
             
             
             
             
2. 解决上述问题中，发现 quote 不能处理中文 UNICODE 
             
   解决方法:  
             1.把 tag_name encode 成为  UTF-8 串
             2.  quote 之
             3.  在view 中 ，capture 到 tag_name
             4.  先直接转化成 str (URL CAPTURE 到的是 UTF-8的字符串)
             5.  unqoute 之
             6.  decode utf-8 
             7.  此时就可以拿到 原始的 中文 tag_name in unicode  format
             