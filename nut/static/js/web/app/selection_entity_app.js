require([
        'libs/polyfills',
        'jquery',
        'utils/EntityLike',
        'subapp/topmenu',
        //'subapp/loadentity',
        'subapp/gotop',
        'subapp/scrollview_selection',
    ],

    function (polyfill,
              jQuery,
              AppEntityLike,
              Menu,
              ScrollEntity,
              GoTop) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var app_like = new AppEntityLike();
        var app_scrollentity = new ScrollEntity();
        var goto = new GoTop();
    });
