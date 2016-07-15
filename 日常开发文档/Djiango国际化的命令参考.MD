本机： 开发测试机
服务器： 果库的 test server , 本文撰写时 IP 为 48

－3. 本机执行 ./manage.py makemessages -l zh_CN


－2. 本机做好 po 文件翻译工作， FUZZY 的翻译要做好处理

－1. 本机执行 ./manage.py compilemessages
     重新启动本机测试server，确保翻译正确显示

－0.5     
     更新github 代码
     commit change
     git push origin dev 
     

0.  上传最新版本的代码到测试服务器
    project_dir/deploy/fab -f upload_test.py upload 
    需要输入密码。
    


1.  登录到测试服务器 (注意命令大小写）
    翻译有更新的情况下,需要重新启动服务器.
    
    
    
   