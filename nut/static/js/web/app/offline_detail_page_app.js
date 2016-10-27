
require([
        'libs/polyfills',
        'jquery',
        'subapp/topmenu',
        'subapp/user_follow',
        'subapp/offline_shop/show_map',
        'subapp/entitylike'
    ],
    function(polyfill,
             jQuery,
             Menu,
             UserFollow,
             ShowMap,
              AppEntityLike

    ){
        var menu = new Menu();
        var user_follow = new UserFollow();
        var show_map = new ShowMap();
        var app_like = new  AppEntityLike();
    });
