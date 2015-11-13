require([
        'libs/polyfills',
        'jquery',
        'subapp/page',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/detailsidebar',
        'subapp/entitylike',
        'libs/csrf'

    ],
    function (polyfill,
              jQuery,
              Page,
              Menu,
              GoTop,
              SideBarManager,
              EntityLike

    ){
        var page = new Page();
        var menu = new Menu();
        var goto = new GoTop();
        var sidebar = new SideBarManager();
        var entityLike  =new EntityLike();
        console.log("entity detail init！");
});
