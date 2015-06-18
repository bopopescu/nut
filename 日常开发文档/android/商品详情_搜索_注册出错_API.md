
1 . 商品详细信息中 的  数据 
    http://api.guoku.com/mobile/v4/entity/{{ entity id  }}/
    返回值
      {
        entity :  商品对象  
        note_list : 点评列表， 数组
        like_user_list: 喜爱用户列表
      }
      
 ## entity.like_count  , 喜欢用户计数
 ## entity.note_count  , 商品点评计数
 ## 喜欢用户列表 就是 like_user_list, 
 
 

2. 搜索页 
       搜索商品 : 
       http://api.guoku.com/mobile/v4/entity/search/
       
       METHOD :  GET
      ## 传入参数 : 
            {
                type :  ‘like’ 或 空
                offset:  绝对偏移量 
                count:   每页数量
            }
       当 type = like  , 搜索的是用户喜爱的商品
          type 为空    , 搜素的是所有用户商品
       
      ## 返回: {
            state: {
                all_count : 搜索结果的商品数量
                like_count : 在type == 'like' 时, 结果商品的数量
            }
      }
      
      搜索用户:
       http://api.guoku.com/mobile/v4/user/search/
       
       METHOD :GET 
       ## 传入参数
       {
           offset: 绝对偏移
           count: 每页的数量
       }
      
      
－－－－－－－－－－－－－－－－－－－－－－－
    offset 和 count 的 源代码
    
    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))
    _key = request.GET.get('session')

    if _offset > 0 and _offset < 30:
        return ErrorJsonResponse(status=404)

    // 注意这里 ---------- 计算页数 
    _offset = _offset / _count + 1
    
    paginator = ExtentPaginator(results, _count)
    users = paginator.page(_offset)
    
    
    
－－－－－－－－－－－－－－－－－－－－－－－ 
    搜索标签 ： 
        没有搜索标签！！！！， 改为搜索品类
    搜索品类： 
       1 ， 拿到 category list 
       http://api.guoku.com/mobile/v4/category/
       返回值  数组， 所有父品类的列表
       ----------------------
       def category_list(request):
            res = Category.objects.toDict()
            # res = []
            return SuccessJsonResponse(res)
       ----------------------
       2. 拿到子品类
       父品类的  sub_categories 属性中有所有自品类的列表
       3. 拿到子品类的 ICON
       自品类的 ICON 属性，
       4.子品类需要隐藏， 看 status 字段
       --------------------
       class Sub_Category(BaseModel):
            group = models.ForeignKey(Category, related_name='sub_categories')
            title = models.CharField(max_length = 128, db_index = True)
            icon = models.CharField(max_length = 64, db_index = True, null = True, default = None)
            status = models.BooleanField(default = True, db_index = True)
       --------------------
       STATUS 为 FALSE 的隐藏，不被搜索出来
       拿到如上子品类之后，缓存（1天？）
       用户搜索品类在本机 ， 用以上品类数据实现。
       
3.  用户注册 ， 出错信息
      http://api.guoku.com/mobile/v4/register/
      
      返回值{
        type: 错误码
        'message' :  ‘用户提示信息’
      }
      
       
        
        
       