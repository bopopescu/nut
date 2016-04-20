require([
        'jquery',
        'subapp/topmenu',
        'subapp/store/store_banner',
        'subapp/store/annual_report',
        'subapp/store/entity_slick'
    ],
    function (
              jQuery,
              Menu,
              StoreBanner,
              AnnualReport,
              EntitySlick
    ){
        var menu = new Menu();
        var store_banner = new StoreBanner();
        var annual_report = new AnnualReport();
        var entity_slick = new EntitySlick();
});

