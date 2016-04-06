
require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/user_follow'
    ],
    function(polyfill,
             jQuery,
             AppEntityLike,
             Menu,
             GoTop,
             UserFollow

    ){
        var app_like = new  AppEntityLike();
        var menu = new Menu();
        var goto = new GoTop();
        var user_follow = new UserFollow();
    });
