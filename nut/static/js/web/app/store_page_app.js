require([
        'jquery',
        'subapp/topmenu',
        'subapp/store/store_banner',
        'subapp/store/annual_report'
    ],
    function (
              jQuery,
              Menu,
              StoreBanner,
              AnnualReport
    ){
        var menu = new Menu();
        var store_banner = new StoreBanner();
        var annual_report = new AnnualReport();
});

