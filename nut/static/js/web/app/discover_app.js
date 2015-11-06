requirejs.config({
    baseUrl:base_url,
    paths: {
        libs: './libs',
        subapp: './subapp',
        jquery: 'libs/jquery-1.11.1.min',
        bootstrap: 'libs/bootstrap.min',
        fastdom: 'libs/fastdom',
        cookie: 'libs/jquery.cookie',
        utils: './utils'
    },

    shim: {
        'cookie':{
            deps:['jquery']
        },
        'bootstrap':{
            deps:['jquery']
        },
        'jquery':{
            exports:'jQuery'
        }
    }
});

require([
        'libs/polyfills',
        'jquery',
        'utils/EntityLike',
        'subapp/topmenu'
    ],
    function(polyfill,
             jQuery,
             AppEntityLike,
             Menu
    ){
        var menu = new Menu();
        var app_like = new  AppEntityLike();
    });
