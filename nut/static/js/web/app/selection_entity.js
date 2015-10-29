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
        underscore:'libs/underscore'

    },

    shim: {
// shim won't handle script load , you still need require script in your source

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
         'subapp/loadentity'
        ],
        function(jQuery,
                 AppEntityLike,
                 Menu,
                 LoadEntity){
// TODO : check if csrf work --
// TODO : make sure bind is usable
 var  menu = new Menu();
 var  app_like = new  AppEntityLike();
 var  app_loadEntity = new LoadEntity();
      console.log(jQuery);

});