require([
        'jquery',
        'subapp/topmenu',
        'subapp/gotop'
    ],
    function (
        jQuery,
        Menu,
        GoTop) {
        var menu = new Menu();
        var goto = new GoTop();
    });
