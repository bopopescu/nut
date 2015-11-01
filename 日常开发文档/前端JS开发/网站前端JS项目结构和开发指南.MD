
需要达到目的 ： 
==================   
   1. 通过requirejs, 来处理前端模组化开发需求
   2. 通过 grunt 来自动化开发过程
      1. jshint(too much syntax error,in our js, closed for now)
      2. requirejs build
      3. test( not implement ye)
   3. 通过 bower 来管理外部库依赖（ NOT implement yet）
   
   
遥远的未来： 
    4. auto TEST SUIT (with phantom/casper)
    5. CI (tri/jenkins )
    6. MVVM 
      

getting started:
===================
1. cd  static/js/web/
2. npm install (need node.js installed globally)
3. grunt watch 
   
   then grunt will monitor all sub dir js change 
   and compile/build production files 
   
   for now only entity_selection use this method 
   other page still use old method , 
   will migrate page by page
   






   
   
文件结构策略： 
====================
   每个页面各自有不同的 ***_app.js
   （例如 : selection 页的主文件为 selection_entity_app.js）
   
   开发的时候通过 requirejs 管理依赖，
   源文件放入 app目录中，
   
   
   利用 requirejs 的 optimizer 输出到 build目录中。
   (例如：selection_entity_app.js 会编译成为 selection_entity_app_build.js)
   文件名称会加上 "_build".
   
   Django 模版文件需要引用 build 好的文件（生产系统）
          测试系统用未优化的文件。(TODO : automation）
          

实现细节
===============================
1. 网站前端（不包含管理界面）项目位置
    nut/static/js/web

2. 目录内容说明 
   a. app  ： 源代码
   b. build  ： 发布代码（用requireJS , brunt自动编译）
      注意：django 模版中引用的应该是 build 目录下的文件
      
   C. node_modules 
      在 /nut/static/js/web 路径下运行 npm install 
      由于 package.json 文件的存在， 系统会自动安装需要的工具：grunt 和插件等等
      
   d. gruntfile.js 
      http://gruntjs.com/configuring-tasks
      
   e.   
   
相关文章和资源：

grunt,bower,requirejs

