1.  数据请求地址:
    http://www.guoku.com/design_week/2016/
    尚未开通
    
2.  请求方法: GET

3.  请求参数: 
    例子: 
        http://www.guoku.com/design_week/2016/?page_offset=3&page_size=20
        
    page_offset: int  #第*页 (1 起步)
    page_size: int    #每页的商品数
    
4.  返回数据格式:JSON
    例子
    {
        total_count: 230,
        page_offset:3,
        page_size: 20,
        data:[
            {
               image:'http://imgcdn.guoku.com/images/few23432423.jpg',
               title: 'AZT design 通勤自行车',
               price: 2399.00,
               liked: 123, 
               url: 'http://www.guoku.com/detail/2342fe0e/'
            },
            {
               image:'http://imgcdn.guoku.com/images/few23432423.jpg'
               title: 'AZT design 通勤自行车',
               price: 2399.00,
               liked: 123, 
               url: 'http://www.guoku.com/detail/2342fe0e/'
            }
            .
            .
            .
            .
            .
            .
            .
        ]
    }
   
    字段解释: 
        image: 商品图
        title: 商品名称
        price: 商品价格
        liked: 喜爱数字(果库喜爱类似收藏)
        url:   商品详情链接
        