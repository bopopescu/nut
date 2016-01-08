require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/header',
        'subapp/yearseller/linkscroll',
        'subapp/yearseller/share',
        'cookie',
        'subapp/top_ad/top_ad'
    ],
    function(polyfill,
             $,
             YearSellerHeader,
             AnchorScroller,
             ShareHanlder,
             cookie,
             TopAd

    ){

        var sellerHeader = new YearSellerHeader();
        var anchorScroller = new AnchorScroller('.sections-titles-wrapper li a');
        var shareHandler = new ShareHanlder();
        var topAd = new TopAd();
        console.log('in year seller app');

    });
