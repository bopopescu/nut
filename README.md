[![guoku icon](http://tp4.sinaimg.cn/2179686555/50/5657509044/1)](id:jiaxin)


## 概览
**果库网站 V4**

### 系统环境
* Ubuntu 
* Python2.7 
* MySQL 
* Nginx 
* Redis

### 快速安装
 ```
 virtualenv guoku-v4
 source /path/to/guoku-v4/bin/active
 pip install -r requirements.txt
 ```


### 后端框架
* *django-1.6.5* [相关文档](https://docs.djangoproject.com/en/1.6/)

### 前端框架
* *bootstrap-3.2.0* [相关文档](http://getbootstrap.com/)
* *jQuery-1.11.1*	[相关文档](http://jquery.com/)

### 安装包
* *django-storage （果库开发）*  [https://github.com/guoku/django-storages.git](https://github.com/guoku/django-storages.git)
* *MySQL-python*
* *django-debug-toolbar*
* *Wand* [相关文档](http://docs.wand-py.org/en/0.3.7/)

### Debug 工具
* *django-debug-toolbar* [相关文档](http://django-debug-toolbar.readthedocs.org/en/1.2/installation.html#quick-setup)

### 部署到服务器
* deploy 目录结构

```
deploy/
├── config.ini
├── guoku.pass
├── reload_server.py
├── update_online_code.sh
└── upload_code.py
```

* *config.ini* 配置文件
* *guoku.pass* 密码文件
* *reload_server.py* 重启服务
* *upload_code.py* 上传代码
* *update_online_code.sh* 更新代码 并且重启服务 


```
pip install fabric
cd deploy/
sh update_online_code.sh
```


### Emial
 <jiaxin@guoku.com>
