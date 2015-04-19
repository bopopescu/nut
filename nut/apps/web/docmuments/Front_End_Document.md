2015-4-19
1. 关于果库顶部导航条中， 专题链接 ， 右上方的红点的显示问题
    需求：
       a): 后端： 用户访问果库时，读取最新的 event slug， 放到页面中的一个script tag 中， 
           定义global var newest_event_slug. 这个值就是最新的在显示中的 event slug
           a.1) : 缓存这个值 ， timeout=3*3600 sec
                  TODO
                  
                  https://docs.djangoproject.com/en/1.8/topics/cache/
           
           a.2) : for put a var in all page ( newest_event_slug), we should set the
                  TEMPLATE_CONTEXT_PROCESSORS value in settings.py 
                  
                  http://www.djangobook.com/en/2.0/chapter09.html
                  
           a.3) 需要修改SETTING文件，TEMPLATE_CONTEXT_PROCESSORS 中加入 lastslug  processor
            
                  
                             
           
           
       b): 前端： 读取用户cookie , KEY = "viewed_event_slug", 
           这个值应该是个list, 但是由于现在的实现中， 只有一个active的slug，因此
           这个值现在只是一个字符串。
       c): 前端：对比 cookie中的 viewed_event_slug, 和 global var 中的 newest_event_slug
           如果两者相等， 那么不需要显示红点， 如果不相等，那么需要显示红点
           
       d): 当用户访问 http://www.guoku.com/event/ ，（目前会读取最新的event, 并显示之）， 
           在template='web/events/home'中， 设置cookie , KEY = "viewed_event_slug" = global var newest_event_slug
           
       ___future___:
          
       f): 接下来的问题是， 当 ， 需要显示历史的 专题内容， 那时候需要建立一个 新的数据表， 
           纪录用户看过的 专题 ， 前端读取 newest_event_slug, 随后 ajax call 后台查询出用户有无看过 该篇 专题
           如果没有，显示红点，如果有，则不用显示
           完毕。
           

2.   TODO
      <script src="{% static 'js/html5shiv.min.js' %}"></script>
      <script src="{% static 'js/respond.min.js' %}"></script>
      这两个文件在哪里？
    