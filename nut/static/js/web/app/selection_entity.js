require.config({
    baseUrl: base_url,
    paths: {
        libs: './libs',
        utils: './utils',
        subapp: './subapp',
        jquery: 'libs/jquery-1.11.1.min',
        bootstrap: 'libs/bootstrap.min',
        fastdom: 'libs/fastdom',
        csrf:'libs/csrf',
        underscore:'libs/underscore',
        cookie: 'libs/jquery.cookie'
    },

    shim: {
// shim won't handle script load , you still need require script in your source
        'cookie':{
            deps:['jquery']
        },
        'csrf':{
            deps:['jquery']
        },
        'bootstrap':{
            deps:['jquery']
        },
        'jquery':{
            exports:'jQuery'
        },
        'underscore':{
            exports: '_'
        }
    }


});


require(['jquery',
         'utils/EntityLike',
         'subapp/topmenu',
         'subapp/loadentity',
         'subapp/gotop',
        ],
        function(jQuery,
                 AppEntityLike,
                 Menu,
                 LoadEntity,
                 GoTop
        ){
// TODO : check if csrf work --
// TODO : make sure bind is usable
         var  menu = new Menu();
         var  app_like = new  AppEntityLike();
         var  app_loadEntity = new LoadEntity();
         var  goto = new GoTop();

});