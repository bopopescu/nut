requirejs.config({
    baseUrl:base_url,
    paths: {
        libs: './libs',
        utils: './utils',
        subapp: './subapp',
        jquery: 'libs/jquery-1.11.1.min',
        bootstrap: 'libs/bootstrap.min',
        fastdom: 'libs/fastdom.ant',
        csrf:'libs/csrf',
        underscore:'libs/underscore.ant',
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

require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/loadentity',
        'subapp/gotop',
    ],
    function (polyfill,
              jQuery,
              AppEntityLike,
              Menu,
              LoadEntity,
              GoTop) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var app_like = new AppEntityLike();
        var app_loadEntity = new LoadEntity();
        var goto = new GoTop();
    });


