require([
        'jquery',
        'subapp/topmenu',
        'subapp/store/store_banner',
        'subapp/user_follow'
    ],
    function (
              jQuery,
              Menu,
              StoreBanner,
              UserFollow

    ){
        var menu = new Menu();
        var store_banner = new StoreBanner();
        var user_follow = new UserFollow();

});

