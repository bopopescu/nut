
require([
        'libs/polyfills',
        'jquery',
        'subapp/topmenu',
        'subapp/user_follow'
    ],
    function(polyfill,
             jQuery,
             Menu,
             UserFollow

    ){
        var menu = new Menu();
        var user_follow = new UserFollow();
    });
