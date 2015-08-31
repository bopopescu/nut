1. 安装

   need install bleach package 
   pip install bleach 
   
   文件 requirements 中加入一行 
   bleach==1.4.1
   
1.5 数据准备

2.  目前允许的 TAG 
    ['p', 'em', 'strong', 'div', 'ul', 'ol', 'li','a','br','span','img']
    
    目前允许的  attribute
    {
    '*': ['class'],
    'a': ['href', 'rel'],
    'img': ['src', 'alt'],
    }



3.  测试FEED 地址
    https://feedvalidator.flipboard.com/
   
    测试 feed : http://www.guoku.com/feed/articles/
         
    1. Feed is missing a PubSubHubbub URL
    2. 图片比例不对： 
       Flipboard 要求 2:1 比例以下 （如 1.5 :1 )
       太扁的图片不支持
    3. 图片尺寸不支持 
       目前商品卡片的图片 宽 240 ， Flipboard 要求最少 400 宽
       
    以上都是   
    


    
    
    

    