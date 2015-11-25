require([
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop',
    ],
    function (
              jQuery,
              AppEntityLike,
              Menu,
              GoTop) {
        var menu = new Menu();
        var app_like = new AppEntityLike();
        var goto = new GoTop();
    });


