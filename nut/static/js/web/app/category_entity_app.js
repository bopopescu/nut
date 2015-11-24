require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/load_category_entity',
        'subapp/gotop',
    ],
    function (polyfill,
              jQuery,
              AppEntityLike,
              Menu,
              LoadCategoryEntity,
              GoTop) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var app_like = new AppEntityLike();
        var app_load_category_entity = new LoadCategoryEntity();
        var goto = new GoTop();
    });
