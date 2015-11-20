require([
        'libs/polyfills',
        'jquery',
        'subapp/page',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/detailsidebar',
        'subapp/entitylike',
        'subapp/entityreport',
        'subapp/note/usernote',
        'libs/csrf'

    ],
    function (polyfill,
              jQuery,
              Page,
              Menu,
              GoTop,
              SideBarManager,
              EntityLike,
              EntityReport,
              UserNote
    ){
        var page = new Page();
        var menu = new Menu();
        var goto = new GoTop();
        var sidebar = new SideBarManager();
        var entityLike  =new EntityLike();
        var entityReport = new EntityReport();
        var userNote = new UserNote();
        console.log("entity detail init");
});
