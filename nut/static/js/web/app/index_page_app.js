require([
        'libs/polyfills',
        'jquery',
        'subapp/topmenu',
        'subapp/index/banner'

    ],

    function (polyfill,
              jQuery,
              Menu,
              Banner
              ) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var banner = new Banner();
    });
