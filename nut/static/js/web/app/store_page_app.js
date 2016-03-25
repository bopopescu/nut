require([
        'jquery',
        'subapp/topmenu',
        'subapp/store/store_banner',
        'subapp/store/annual_report',
        'subapp/user_follow'
    ],
    function (
              jQuery,
              Menu,
              StoreBanner,
              AnnualReport,
              UserFollow

    ){
        var menu = new Menu();
        var store_banner = new StoreBanner();
        var annual_report = new AnnualReport();
        var user_follow = new UserFollow();

});

