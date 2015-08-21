URL : mobile/v4/user/update/email/ 
Input : 
    param :  post 
    {
        password : 老密码
        email: 新邮箱
        
    }
Output: 
   成功 ： 返回用户信息 JSON
   失败 ： {
        type: 失败类型
        message: 失败描述
   } status = 400 
   
   有的时候程序出错 会返回500，
   