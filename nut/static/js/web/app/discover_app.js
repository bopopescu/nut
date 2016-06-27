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
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/discover/category_slick',
        'subapp/discover/recommend_user_slick'
    ],
    function(polyfill,
             jQuery,
             AppEntityLike,
             Menu,
             CategorySlick,
             RecommendUserSlick
    ){
        var menu = new Menu();
        var app_like = new  AppEntityLike();
        var category_slick = new CategorySlick();
        var recommend_user_slick = new RecommendUserSlick();
    });
