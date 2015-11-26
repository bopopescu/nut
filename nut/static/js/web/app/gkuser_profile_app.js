require([
        'jquery',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/user_follow'
    ],

    function (
        jQuery,
        Menu,
        UserFollow,
        GoTop) {
        var menu = new Menu();
        var goto = new GoTop();
        var user_follow = new UserFollow();
    });
