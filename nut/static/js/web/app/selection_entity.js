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
         'subapp/topmenu'
        ],
        function(jQuery,
                 AppEntityLike,
                 Menu

    ){
// TODO : check if csrf work --
//
 var  menu = new Menu();
 var  app_like = new  AppEntityLike();
      console.log(jQuery);

});