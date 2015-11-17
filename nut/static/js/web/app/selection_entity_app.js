require([
        'libs/polyfills',
        'jquery',
        'utils/EntityLike',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/scrollview_selection',
        'masonry',
        'jquery_bridget'
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
