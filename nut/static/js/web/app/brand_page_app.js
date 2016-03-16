
require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop'
    ],
    function(polyfill,
             jQuery,
             AppEntityLike,
             Menu,
             GoTop
    ){
        var app_like = new  AppEntityLike();
        var menu = new Menu();
        var goto = new GoTop();
    });
