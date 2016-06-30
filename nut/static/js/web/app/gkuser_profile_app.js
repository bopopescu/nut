require([
        'jquery',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/user_follow',
         'subapp/user_profile/authorized_author_share'
    ],

    function (
        jQuery,
        Menu,
        UserFollow,
        GoTop,
        AuthorizedAuthorShare) {
        var menu = new Menu();
        var goto = new GoTop();
        var user_follow = new UserFollow();
        var authorized_author_share = new AuthorizedAuthorShare();
    });
