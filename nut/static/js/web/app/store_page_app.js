require([
        'jquery',
        'subapp/topmenu',
        'subapp/store/store_banner',
        'subapp/store/annual_report',
        'subapp/store/entity_slick',
        'subapp/user_follow'
    ],
    function (
              jQuery,
              Menu,
              StoreBanner,
              AnnualReport,
              EntitySlick,
              UserFollow
    ){
        var menu = new Menu();
        var store_banner = new StoreBanner();
        var annual_report = new AnnualReport();
        var entity_slick = new EntitySlick();
         var user_follow = new UserFollow();
});

