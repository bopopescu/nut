<p align="center">
  <img title="backbone marionette" src='http://tp4.sinaimg.cn/2179686555/50/5657509044/1' />
</p>

<p align="center">The Django framework</p>

## 概览
**果库网站 V4**

### 系统环境
* Ubuntu 
* Python2.7 
* MySQL 
* Nginx 
* Redis

### 安装 MySQL
```
brew install mysql
```

### 安装 ImageMagick
```
brew install imagemagick
```

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


<!--### 搜索引擎
* *whoohe-2.5.6* [相关文档](https://pythonhosted.org/Whoosh/index.html)-->


### 安装包
* *django-storage （果库开发）*  [https://github.com/guoku/django-storages.git](https://github.com/guoku/django-storages.git)
* *MySQL-python*
* *django-debug-toolbar*
* *Wand* [相关文档](http://docs.wand-py.org/en/0.3.7/)

### 分词
* "结巴"中文分词 [相关文档](https://github.com/fxsjy/jieba)
```
pip install jieba
```


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

## Models 与 Cache 之间的关系

＊ 以获取热门商品为例：

利用 django models queryset 实现扩展的 SQL 查询。 Manager 方法来实现缓存。 以减少 models 层面的改动，而影响 views.

```
class EntityLikeQuerySet(models.query.QuerySet):

    def popular(self):
        dt = datetime.now()
        days = timedelta(days=7)
        popular_time = (dt - days).strftime("%Y-%m-%d") + ' 00:00'
        return self.filter(created_time__gt=popular_time).annotate(dcount=models.Count('entity')).values_list('entity_id', flat=True)

    def user_like_list(self, user, entity_list):

        return self.filter(entity_id__in=entity_list, user=user).values_list('entity_id', flat=True)


class EntityLikeManager(models.Manager):

    def get_query_set(self):
        return EntityLikeQuerySet(self.model, using=self._db)

    def popular(self):
        res = cache.get('entity_popular')
        if res:
            return res
        res = self.get_query_set().popular()
        cache.set('entity_popular', res, timeout=3600)
        return res

    def user_like_list(self, user, entity_list):

        return self.get_query_set().user_like_list(user=user, entity_list=entity_list)
```


## 导出数据
```
/opt/mysql5/bin/mysqldump --single-transaction --flush-logs -u root core --ignore-table=core.core_entity_like --ignore-table=core.notifications_notification > core.sql
```

### Email
 <jiaxin@guoku.com>
