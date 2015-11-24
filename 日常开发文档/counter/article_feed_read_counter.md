1. ever article feed will be appended a img html 
    see:  models.Article.feed_content

2. every time user read feed article , img will be shown to the user 
   this img will trigger counter 
    
    see: apps/counter/views/__init__.py
    
3. img contains the article id , which will be saved(incr) to cache with a unique key for that article 
   see 2 
   
4. every time a key for article is incred , the article id   will be added to a set , 
   this set is also been cached 
   the set contain all article id , need to be synced with mysql table , core_article , for column feed_read_count

5. once in a while (about 30 min) 
   a script will be runed (nut/script/counter/article_feed_counter_save.py)
   in the script :
            a. get the set of id , from the set mentioned in 4
            b. update those article's feed_read_count by the value in cache
            c. clear the set , wait for the next run 
            
6. when feed is generated for individual article 
   feed_count_img will be added to the bleached content of the article 
   to get the feed_count_img url 
        reverse it from the counter url 
        see : /nut/apps/counter/urls/__init__.py
        
        
7. deploy cron_tab     

3. sudo crontab -e   , 打开的编辑器里加入下面一行,并保存

*/30 * * * * /usr/local/bin/python /data/www/nut/script/counter/article_feed_counter_save.py 
 