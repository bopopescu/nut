1. 安装

   need install bleach package 
   pip install bleach 
   
   文件 requirements 中加入一行 
   bleach==1.4.1
   
1.5 去除空的 
    <P></P>

1.6 将商品卡片中的相对链接换成绝对链接
    href="/detail/......./" ---> href="http://www.guoku.com/detail/....../"

1.7 将 style='font-weight: bold'  的 SPAN tag , 替换成为 <b>

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
       目前商品卡片的图片 宽 240 ， Flipboard 要求最少 400 宽,  因此商品卡片的图片会被屏蔽。
       
       
       
    以上都是   
    


    
    
    

    