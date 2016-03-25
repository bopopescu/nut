###EDM

####Related Files:
* nut/nut/apps/core/models.py
* nut/nut/apps/core/tasks/edm.py
* nut/nut/apps/management/views/edm.py

####Features

后台的操作都是通过Sendcloud的API进行操作。sendcloud地址：

[http://sendcloud.sohu.com/email/](http://sendcloud.sohu.com/email/)

用户名：app@guoku.com

密码：Comguoku1@#

查看sendcloud相关API：

[http://sendcloud.sohu.com/doc/guide/base/](http://sendcloud.sohu.com/doc/guide/base/)
    
####地址列表

首先，我们会维护一个在sendcloud的地址列表。该地址列表包含所有通过了邮箱验证的果库用户的邮件地址。查看地址列表：

[http://sendcloud.sohu.com/email/#/sendAround/mailList](http://sendcloud.sohu.com/email/#/sendAround/mailList)
  
###### 用户注册  
* 当用户注册后，会通过sendcloud给用户发一封激活邮件。当用户点击了激活邮件中的链接后：

  * 把该用户的邮件地址加入到邮件列表中
  * 把该用户的email_verified改为True

*这部分代码在 nut/nut/apps/core/models.py: line 1891*
    
*会调用 nut/nut/apps/core/tasks/edm.py中的task*

###### 修改邮箱
* 当用户修改邮箱地址的时候：
  * 首先根据用户名把旧的邮箱从sendcloud的地址列表中删除
  * 通过sendcloud发一封激活邮件给新的邮箱地址
  * 把该用户的email_verified改为False
  * 如果用户点了激活邮件，则重复上面[用户注册]的步骤。
  
*这部分代码在 /nut/nut/apps/core/models.py: line 444*
*会调用nut/nut/apps/core/tasks/edm.py中的task*


------
####EDM模板
后台根据固定格式，创建一个EDM模板。地址：

[http://www.guoku.com/management/edm/](http://www.guoku.com/management/edm/)
    
*这部分代码在：nut/nut/apps/management/views/edm.py*

*ps: 每次都要重新创建模板的原因是因为，邮件的每一张图都要通过sendcloud的审核，所以没办法把图片地址作为变量替换。*

在页面上点击添加并添加成功后，在sendcloud中可以看到新建的模板：

[http://sendcloud.sohu.com/email/#/sendAround/template](http://sendcloud.sohu.com/email/#/sendAround/template)

创建好模板后，需要等待sendcloud审核。此时后台页面中这个EDM的状态为"等待审核"，点击"检查审核"按钮，会调用sendcloud的一个API，检查这个模板的审核状态。一般审核时间会是一小时以内。
如果审核通过，会有一个按钮"发送"。点击发送按钮，会通过sendcloud的API把这封EDM发给地址列表中的所有用户。

*ps: 审核通过后的EDM不能再次修改，如果修改了需要重新提交审核*

#####查看发送情况

发送成功后，想看发送情况，在这里看：

[http://sendcloud.sohu.com/email/#/data/send](http://sendcloud.sohu.com/email/#/data/send) 趋势 

[http://sendcloud.sohu.com/email/#/response/status](http://sendcloud.sohu.com/email/#/response/status) 成功/失败
    